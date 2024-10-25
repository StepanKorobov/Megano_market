from django.contrib.auth.models import User
from django.db import models

from goods.models import Product


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    session_key = models.CharField(
        max_length=255, default="default_session_key", null=True
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "session_key", "product")
