from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
import random
from decimal import Decimal


# Customize the user model
class UserBank(AbstractUser):
    ssn = models.CharField(max_length=11, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True, verbose_name="Phone Number")


# Accounts model
class Account(models.Model):
    ACCOUNT_TYPE = [
        ('Checking', 'Checking'),
        ('Saving', 'Saving'),
        ('Credit Card', 'Credit Card'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="accounts",
        verbose_name="User",
    )
    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE,
        verbose_name="Account Type",
    )

    account_number = models.CharField(
        max_length=16,
        unique=True,
        editable=False,
        verbose_name="Account Number"
    )

    account_password = models.CharField(
        max_length=128,
        verbose_name="Account Password",
        help_text="Password for this account. It is separate from your login password.",
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Balance",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
    )

    # Locked_account
    is_locked = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Account"

    def __str__(self):
        return f"{self.user.username} - {self.account_type} Account"

    def save(self, *args, **kwargs):
        if not self.account_number:
            # generate the unique account number
            self.account_number = str(random.randint(10 ** 15, 10 ** 16 - 1))
        super().save(*args, **kwargs)

    def set_account_password(self, raw_password):
        """
        using django password to store the password
        """
        self.account_password = make_password(raw_password)

    def check_account_password(self, raw_password):
        """
        Verify the account and password
        """
        return check_password(raw_password, self.account_password)

    def deposit(self, amount):
        """
        deposit
        """
        amount = Decimal(amount)
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        """
        withdraw
        """
        amount = Decimal(amount)
        self.balance -= amount
        self.save()
