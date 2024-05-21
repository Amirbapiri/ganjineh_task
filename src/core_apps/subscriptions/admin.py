from django.contrib import admin

from .models import SubscriptionPlan, UserSubscription, CreditIncreaseRequest, MonthlyLimitIncreaseRequest


admin.site.register(SubscriptionPlan)
admin.site.register(UserSubscription)
admin.site.register(CreditIncreaseRequest)
admin.site.register(MonthlyLimitIncreaseRequest)
