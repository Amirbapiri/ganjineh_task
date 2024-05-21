from datetime import date, timedelta
from rest_framework import status, views, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from .permissions import (
    IsAdminUser,
    HasActiveSubscription,
    RegularUserPermission,
    SpecialSubscribedUserPermission,
    SubscribedUserPermission,
)
from core_apps.tokens.models import TokenPrice
from core_apps.profiles.models import Profile
from core_apps.tokens.tasks import process_csv_upload
from core_apps.tokens.signals import insufficient_signal_notification
from core_apps.subscriptions.models import UserSubscription


class TokenDataUploadView(views.APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        token_name = request.data.get("token_name")

        try:
            file_content = file.read()
            process_csv_upload.delay(file_content, token_name)
            return Response(
                {"detail": "Data uploaded successfully"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegularUserProfitView(views.APIView):
    permission_classes = (
        permissions.IsAuthenticated,
        RegularUserPermission | SubscribedUserPermission,
    )

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = user.profile
        token_name = request.query_params.get("token_name")

        success, error = profile.check_and_deduct_credits(token_name)
        if not success:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        token_prices = TokenPrice.objects.filter(
            token__name=token_name, date__range=[start_date, end_date]
        ).order_by("date")

        if not token_prices.exists():
            return Response(
                {"error": "No data available for the specified range"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        max_profit, buy_date, sell_date = self.calculate_max_profit_range(token_prices)

        if buy_date and sell_date:
            response_data = {
                "buy_date": buy_date.date,
                "buy_price": buy_date.price,
                "sell_date": sell_date.date,
                "sell_price": sell_date.price,
                "profit": max_profit,
            }
        else:
            response_data = {"error": "No profitable buy/sell pairs found."}

        return Response(response_data)

    def calculate_max_profit_range(self, token_prices):
        if not token_prices:
            return 0, None, None

        min_price_entry = token_prices[0]
        max_profit = 0
        buy_date = None
        sell_date = None

        for price_entry in token_prices:
            if price_entry.price < min_price_entry.price:
                min_price_entry = price_entry

            profit = price_entry.price - min_price_entry.price
            if profit > max_profit:
                max_profit = profit
                buy_date = min_price_entry
                sell_date = price_entry
        return max_profit, buy_date, sell_date


class SubscribedUserProfitView(views.APIView):
    permission_classes = (
        permissions.IsAuthenticated,
        SpecialSubscribedUserPermission,
    )

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = user.profile
        token_name = request.query_params.get("token_name")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        success, error = profile.check_and_deduct_credits_for_special_user(amount=10)
        if not success:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        token_prices = TokenPrice.objects.filter(
            token__name=token_name,
            date__range=[start_date, end_date],
        ).order_by("date")

        if not token_prices.exists():
            return Response(
                {"error": "No data available for the specified range"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        top_profits = self.calculate_top_intervals(token_prices, top_n=6, profit=True)
        top_losses = self.calculate_top_intervals(token_prices, top_n=6, profit=False)
        response_data = {
            "top_profits": [
                {
                    "buy_date": buy_date.date,
                    "buy_price": buy_date.price,
                    "sell_date": sell_date.date,
                    "sell_price": sell_date.price,
                    "profit": sell_date.price - buy_date.price,
                }
                for buy_date, sell_date in top_profits
            ],
            "top_losses": [
                {
                    "buy_date": buy_date.date,
                    "buy_price": buy_date.price,
                    "sell_date": sell_date.date,
                    "sell_price": sell_date.price,
                    "loss": sell_date.price - buy_date.price,
                }
                for buy_date, sell_date in top_losses
            ],
        }

        return Response(response_data)

    def deduct_credits(self, profile, amount=10):
        if profile.credits_remaining >= amount:
            profile.credits_remaining -= amount
            profile.save()
            return True
        else:
            insufficient_signal_notification.send(
                sender=self.__class__,
                user=profile.user,
            )
            return False

    def calculate_top_intervals(
        self,
        token_prices,
        top_n=6,
        profit=True,
    ):
        intervals = []

        for i in range(len(token_prices)):
            for j in range(i + 1, len(token_prices)):
                profit_or_loss = token_prices[j].price - token_prices[i].price
                intervals.append((profit_or_loss, token_prices[i], token_prices[j]))

        intervals.sort(reverse=profit, key=lambda x: x[0])

        return [(item[1], item[2]) for item in intervals[:top_n]]
