from django.db import models
from django.conf import settings
from accounts.models import Account

class Transaction(models.Model):
    TRANSACTION_TYPE = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAW', 'Withdraw'),
        ('TRANSFER IN', 'Transfer In'),
        ('TRANSFER OUT', 'Transfer Out'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} by {self.user.username}"
# Create your models here.
