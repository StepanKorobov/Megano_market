from django.urls import include, path

from .views import OrderApiView, OrderViewSet

app_name = "orders"

urlpatterns = [
    path("order/<int:pk>", OrderViewSet.as_view(), name="order"),
    path("orders", OrderApiView.as_view(), name="orders"),
]
