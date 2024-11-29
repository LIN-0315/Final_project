from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Transaction
from accounts.models import Account
from decimal import Decimal

@login_required
def deposit_view(request,account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)  # get account number
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', '0'))
            # If the amount to deposit is smaller than 0, raise an error
            if amount <= 0:
                messages.warning(request, "Deposit amount must be greater than zero. Please try again.")
                raise ValueError()
            else:
                account.deposit(amount)  # Use deposit function in the account view
                Transaction.objects.create(user=request.user, account=account, transaction_type='DEPOSIT', amount=amount)
                messages.success(request, f"Deposited ${amount:.2f} successfully to {account.account_type} account {account.account_number}.")
        except ValueError:
            pass
    # redirect to the deposit view
    return render(request, 'transaction/Deposit.html', {'account': account})

@login_required
def withdraw_view(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)  # get account number
    if request.method == 'POST':
        # If the amount to withdraw is smaller than 0, raise an error
        try:
            amount = Decimal(request.POST.get('amount', '0'))
            if amount < 0:
                messages.warning(request, "Withdraw amount must be greater than zero. Please try again.")
                raise ValueError()
            if account.account_type == 'Credit Card':
                # For credit card, the balance can smaller than 0
                if account.balance - amount < -1000:
                    messages.warning(request, "Insufficient credit limit. Please try again.")
                    raise ValueError()
            else:
                if amount > account.balance:
                    messages.warning(request, "Insufficient balance. Please try again.")
                    raise ValueError()

            account.withdraw(amount)  # Use withdraw function in the account view
            Transaction.objects.create(user=request.user, transaction_type='WITHDRAW', amount=amount)
            messages.success(request,
                             f"Withdraw ${amount:.2f} successfully to {account.account_type} account {account.account_number}.")
        except ValueError:
            pass
    # redirect to the withdrawal view
    return render(request, 'transaction/Withdraw.html', {'account': account})
