from django.urls import path, include
from .views import AddContactAPIView

urlpatterns = [
    path("identify", AddContactAPIView.as_view(), name="identify")
]