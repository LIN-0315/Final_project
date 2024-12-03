from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, AccountCreationForm
from .models import Account
from transactions.models import Transaction
from django.urls import reverse
from decimal import Decimal


# User register
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('create_account')  # redirect to the create new account view
        else:
            messages.error(request, "Registration failed. Please check the form.")
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


# User login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('account_list')  # redirect to account_list
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()  # Initialize the form
    return render(request, 'accounts/login.html', {'form': form})


# user log out
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


# show the accounts for the current user
@login_required
def account_list_view(request):
    if request.method == 'POST':
        account_id = request.POST.get('account_id')
        action = request.POST.get('action')
        amount = request.POST.get('amount')

        account = get_object_or_404(Account, id=account_id, user=request.user)
        amount = float(amount)
        if action == 'deposit':
            account.deposit(amount)
            Transaction.objects.create(
                account=account,
                transaction_type='deposit',
                amount=amount,
            )
            messages.success(request, f"Deposited ${amount:.2f} to {account.account_type} account {account.account_number}.")
        elif action == 'withdraw':
            account.withdraw(amount)
            Transaction.objects.create(
                account=account,
                transaction_type='withdraw',
                amount=amount,
            )
            messages.success(request, f"Withdrew ${amount:.2f} from {account.account_type} account {account.account_number}.")
        return redirect('account_list')
    accounts = request.user.accounts.all()  # get accounts for current user
    for account in accounts:
        if account.account_type == 'Credit Card':
            account.max_credit_available = 1000 + account.balance
    return render(request, 'accounts/account_list.html', {'accounts': accounts})

# create new account
@login_required
def create_account_view(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user  # Link to the current user
            account.set_account_password(form.cleaned_data['account_password'])  # create the password
            account.save()
            messages.success(
                request,
                f"{account.account_type} account created successfully! Account Number: {account.account_number}"
            )
            return redirect('account_list')  # redirect to the account list
    else:
        form = AccountCreationForm()
    return render(request, 'accounts/create_account.html', {'form': form})


# account detail
@login_required
def account_detail_view(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    return render(request, 'accounts/account_detail.html', {'account': account})

@login_required
def transfer_view(request, account_id=None):
    sender_account = None
    if account_id:
        # pre-write the sender account number
        try:
            sender_account = Account.objects.get(id=account_id, user=request.user)
        except Account.DoesNotExist:
            messages.warning(request, "Sender account not found.")
            return render(request, 'accounts/transfer.html', {'sender_account': sender_account})

    if request.method == 'POST':
        sender_username = request.POST.get('sender_username')
        sender_account_number = request.POST.get('sender_account_number')
        sender_account_password = request.POST.get('sender_account_password')
        receiver_account_number = request.POST.get('receiver_account_number')
        amount = Decimal(request.POST.get('amount', '0'))

        # verify transfer amount
        if amount <= 0:
            messages.warning(request, "Transfer amount must be greater than zero.")
            return render(request, 'accounts/transfer.html')

        # verify the account number
        try:
            sender_account = Account.objects.get(account_number=sender_account_number, user=request.user)
        except Account.DoesNotExist:
            messages.warning(request, "Sender account not found.")
            return render(request, 'accounts/transfer.html', {'sender_account': None})

        if not sender_account.check_account_password(sender_account_password):
            messages.warning(request, "Invalid sender password.")
            return render(request, 'accounts/transfer.html')

        # verify enough balance
        if sender_account.balance < amount:
            messages.warning(request, "Insufficient balance.")
            return render(request, 'accounts/transfer.html')

        # verify the receiver account number
        try:
            receiver_account = Account.objects.get(account_number=receiver_account_number)
        except Account.DoesNotExist:
            messages.warning(request, "Receiver account not found.")
            return render(request, 'accounts/transfer.html', {'sender_account': sender_account})

        # transfer
        sender_account.withdraw(amount)
        receiver_account.deposit(amount)

        # create transaction
        Transaction.objects.create(user=request.user,
                                   account=sender_account,
                                   transaction_type='TRANSFER OUT',
                                   amount=amount)

        Transaction.objects.create(user=request.user,
                                   account=receiver_account,
                                   transaction_type='TRANSFER IN',
                                   amount=amount)

        messages.success(request, f"Transferred ${amount:.2f} successfully to account {receiver_account.account_number}.")

    return render(request, 'accounts/transfer.html', {'sender_account': sender_account})


# Locked account view
def account_lock(request, account_id):
    # Get account
    account = get_object_or_404(Account, id=account_id, user=request.user)

    if request.method == 'POST':
        account_password = request.POST.get('account_password')

        # Check password
        if not account.check_account_password(account_password):
            messages.warning(request, "Invalid account password.")
            return render(request, 'accounts/lock.html', {'account': account})

        # Change Lock status
        account.is_locked = not account.is_locked
        account.save()

        # Tell user lock is success
        if account.is_locked:
            messages.success(request, f"Account {account.account_number} has been locked.")
        else:
            messages.success(request, f"Account {account.account_number} has been unlocked.")
        # Redirect to the account_list view when success
        return redirect('account_list')

    # Redirect to the lock view
    return render(request, 'accounts/lock.html', {'account': account})


