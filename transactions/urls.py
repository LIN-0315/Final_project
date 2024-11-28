from django.urls import path
from . import views

urlpatterns = [
    path('deposit/<int:account_id>/', views.deposit_view, name='deposit'),
    path('withdraw/<int:account_id>/', views.withdraw_view, name='withdraw'),
]