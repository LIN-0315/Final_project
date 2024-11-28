from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/', views.account_list_view, name='account_list'),
    path('accounts/create/', views.create_account_view, name='create_account'),
    path('accounts/<int:account_id>/login/', views.account_login_view, name='account_login'),
    path('accounts/<int:account_id>/', views.account_detail_view, name='account_detail'),
]