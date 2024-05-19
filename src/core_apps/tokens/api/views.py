import csv
from datetime import datetime
from rest_framework import status, views, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from .permissions import IsAdminUser
from core_apps.tokens.models import Token, TokenPrice


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
