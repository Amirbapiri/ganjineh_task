from django.urls import path

from .views import TokenDataUploadView, TokenPriceQueryView

urlpatterns = [
    path(
        "upload/",
        TokenDataUploadView.as_view(),
        name="token-data-upload",
    ),
    path(
        "query/",
        TokenPriceQueryView.as_view(),
        name="token-price-query",
    ),
]
