from django.urls import path

from .views import TokenDataUploadView

urlpatterns = [
    path(
        "upload/",
        TokenDataUploadView.as_view(),
        name="token-data-upload",
    ),
]
