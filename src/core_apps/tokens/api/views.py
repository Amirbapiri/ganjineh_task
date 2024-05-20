import csv
from datetime import datetime, date, timedelta
from rest_framework import status, views, permissions, generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from .permissions import IsAdminUser
from core_apps.tokens.models import Token, TokenPrice
from core_apps.profiles.models import Profile
from .serializers import TokenPriceSerializer


class TokenDataUploadView(views.APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        token_name = request.data.get("token_name")

        try:
            token, _ = Token.objects.get_or_create(name=token_name)
            csv_file = csv.DictReader(file.read().decode("utf-8").splitlines())
            for row in csv_file:
                print(row)
                date_str = row.get("Date")
                price = row.get("Price")
                # Convert date to the correct format
                try:
                    date = datetime.strptime(date_str, "%m-%d-%Y").strftime("%Y-%m-%d")
                except ValueError:
                    return Response(
                        {
                            "error": f"Invalid date format for {date_str}. Expected MM-DD-YYYY."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                TokenPrice.objects.update_or_create(
                    token=token,
                    date=date,
                    defaults={"price": price},
                )
            return Response(
                {"detail": "Data uploaded successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RegularUserProfitView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = user.profile
        token_name = request.query_params.get("token_name")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if profile.user_type == Profile.REGULAR:
            if date.fromisoformat(end_date) - date.fromisoformat(
                start_date
            ) > timedelta(days=30):
                return Response(
                    {"error": "Regular users can only query up to one month."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if not self.deduct_credits(profile, token_name):
            return Response(
                {"error": "Insufficient credits"}, status=status.HTTP_400_BAD_REQUEST
            )

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

    def deduct_credits(self, profile, token_name):
        costs = {"btc": 1, "eth": 2, "trx": 3}
        cost = costs.get(token_name.lower())
        if cost is None:
            return False
        if profile.credits_remaining >= cost:
            profile.credits_remaining -= cost
            profile.save()
            return True
        return False

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
