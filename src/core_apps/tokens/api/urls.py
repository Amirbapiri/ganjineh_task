from django.urls import path

from .views import RegularUserProfitView, TokenDataUploadView

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
]
