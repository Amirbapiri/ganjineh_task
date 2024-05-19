from django.db import models


class Token(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class TokenPrice(models.Model):
    token = models.ForeignKey(
        Token,
        on_delete=models.CASCADE,
        related_name="token_prices",
    )
    date = models.DateField()
    price = models.DecimalField(max_digits=20, decimal_places=10)

    class Meta:
        unique_together = (("token", "date"),)

    def __str__(self):
        return f"{self.token} - {self.date} - {self.price}"
