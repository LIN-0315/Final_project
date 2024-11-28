from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, AccountCreationForm
from .models import Account
from transactions.models import Transaction
from django.urls import reverse


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


# login account
@login_required
def account_login_view(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)

    if request.method == 'POST':
        account_password = request.POST.get('account_password')
        if account.check_account_password(account_password):
            # verify the password
            return redirect(reverse('account_detail', args=[account_id]))
        else:
            messages.error(request, "Invalid account password.")

    return redirect('account_list')


# account detail
@login_required
def account_detail_view(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    return render(request, 'accounts/account_detail.html', {'account': account})
