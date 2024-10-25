from django.db import models


class Payment(models.Model):
    """
    Модель для оплаты
    """

    number = models.PositiveIntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    month = models.PositiveIntegerField(blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    code = models.PositiveIntegerField(blank=True, null=True)
