# Generated by Django 4.2 on 2024-05-21 15:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0005_subscriptionplan_monthly_credit_increase_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subscriptionplan",
            name="daily_credits",
        ),
        migrations.RemoveField(
            model_name="usersubscription",
            name="daily_usage",
        ),
    ]
