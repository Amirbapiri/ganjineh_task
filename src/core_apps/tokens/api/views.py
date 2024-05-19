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


class TokenPriceQueryView(generics.ListAPIView):
    serializer_class = TokenPriceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        token_name = self.request.query_params.get("token_name")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        user = self.request.user
        profile = user.profile

        if profile.user_type == Profile.REGULAR:
            if (
                date.fromisoformat(end_date) - date.fromisoformat(start_date)
            ) > timedelta(days=30):
                return Response(
                    {"message": "Regular users can only query up to one month"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if not self.deduct_user_credit(profile, token_name):
            return Response(
                {"message": "Not enough credits"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return TokenPrice.objects.filter(
            token__name=token_name,
            date__range=[start_date, end_date],
        )

    def deduct_user_credit(self, profile, token_name):
        credit_costs = {"btc": 1, "eth": 2, "trx": 3}
        cost = credit_costs.get(token_name.lower())
        if cost is None:
            return False
        if profile.credits_remaining >= cost:
            profile.credits_remaining -= cost
            profile.save()
            return True
        return False
