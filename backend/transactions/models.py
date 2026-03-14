from django.db import models
from django.conf import settings


class MerchantCategoryMap(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    receiver_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.receiver_name} - {self.category}"


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receiver_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.receiver_name} - {self.amount}"