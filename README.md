# Bank System

This project is based on a simulated banking system developed on django server. Allow user to register and log in the system and create different types of accounts, as well as deposit and withdrawal of money, and transfer of money to their own account or to other users' accounts. Accounts also allow users to temporarily lock their accounts as well as delete them.

## How to run the project

First you can create the virtual environment for this project using

```sh
$ python -m venv ENV_DIR
$ source ENV_DIR/bin/activate
$ pip install -r requirements.txt
```

This will ensure that you have the environment, then, you can run

```sh
$ python manage.py runserver
```

on the terminal that opens the project on the http://127.0.0.1:8000/ to the home page.

## Function

### Register and Login

The user can register use the view. There is some restrictions about the password, it needs to be complex.

![image](https://github.com/user-attachments/assets/cb857a84-88d5-428d-b464-c2a910dd21e1)


This is the login page.

![image](https://github.com/user-attachments/assets/dae7092b-0f5a-4c12-8e18-424b8752dbf5)

### Account

Users can create multiple accounts, there are three types of accounts: checking, saving and credit. Each account has its own password. User can lock account and delete account. There is an ACCOUNT model to store account information and correlate it with the database and other models.

### Transfer

Users can deposit and withdraw funds as well as transfer money to other accounts. I use the TRANSACTION model to manage the transfer of deposits and associate it with the account model to manage the amount of deposits under the account.

## Error handling

The system will message the user about some errors, such as deposit and withdrawal amount less than 0, wrong password entry, withdrawal greater than deposit, etc.

## Log out

The users can exit the system by clicking log out.





