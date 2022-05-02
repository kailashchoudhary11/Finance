from asyncio.windows_events import NULL
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from finance import settings
# Create your models here.

class StockUser(models.Model):
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    user = models.CharField(max_length=150, null=False)
    cash = models.DecimalField(max_digits=20, decimal_places=2, null=False, default=10000.00)

    def __str__(self):
        return self.user

class History(models.Model):
    category = models.CharField(max_length=20, null=False)
    price = models.DecimalField(max_digits=20, decimal_places=2, null=False)
    shares = models.IntegerField(null=False)
    symbol = models.CharField(max_length=200, null=False)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(StockUser, on_delete=models.CASCADE)

class AvailableStocks(models.Model):
    user = models.ForeignKey(StockUser, on_delete=models.CASCADE)
    shares = models.IntegerField(null=False)
    symbol = models.CharField(max_length=200, null=False)
