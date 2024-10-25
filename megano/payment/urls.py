from django.urls import path

from .views import PaymentAPIView

app_name = "payment"

urlpatterns = [
    path("payment/<int:pk>", PaymentAPIView.as_view(), name="payment"),
]
