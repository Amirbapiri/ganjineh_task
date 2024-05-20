import csv
from datetime import datetime
from celery import shared_task
from .models import Token, TokenPrice


@shared_task
def process_csv_upload(file_content, token_name):
    token, _ = Token.objects.get_or_create(name=token_name)
    csv_file = csv.DictReader(file_content.decode("utf-8").splitlines())
    for row in csv_file:
        date_str = row.get("Date")
        price = row.get("Price")
        try:
            date = datetime.strptime(date_str, "%m-%d-%Y").strftime("%Y-%m-%d")
        except ValueError:
            return {
                "error": f"Invalid date format for {date_str}. Expected MM-DD-YYYY."
            }

        TokenPrice.objects.update_or_create(
            token=token,
            date=date,
            defaults={"price": price},
        )
    return {"detail": "Data uploaded successfully"}
