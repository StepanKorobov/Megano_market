from django.contrib.auth.models import User
from django.db import models

from goods.models import Product


class Order(models.Model):
    """
    Модель для добавления количества товаров в заказе
    """

    count = models.IntegerField(default=0)
    product = models.ForeignKey(Product, related_name="order", on_delete=models.CASCADE)


class OrdersData(models.Model):
    """
    Модель заказа
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    fullName = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    deliveryType = models.CharField(
        max_length=100, blank=True, null=True, default="ordinary"
    )
    paymentType = models.CharField(
        max_length=100, blank=True, null=True, default="online"
    )
    totalCost = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    status = models.CharField(max_length=16, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    products = models.JSONField(null=True, blank=True)
    # products = models.ManyToManyField(Order, related_name='order_data')

    def __str__(self):
        return f"Tag (PK={self.pk} | user={self.user})"
