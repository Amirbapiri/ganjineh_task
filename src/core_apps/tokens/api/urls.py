from django.urls import path

from .views import RegularUserProfitView, TokenDataUploadView, SubscribedUserProfitView

urlpatterns = [
    path(
        "upload/",
        TokenDataUploadView.as_view(),
        name="token-data-upload",
    ),
    path(
        "regular-user-profit/",
        RegularUserProfitView.as_view(),
        name="regular-user-profit",
    ),
    path(
        "special-user-profit-loss/",
        SubscribedUserProfitView.as_view(),
        name="special-user-profit-loss",
    ),
]
