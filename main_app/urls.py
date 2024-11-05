from django.urls import path
from . import views 

urlpatterns = [
    path('', views.landing, name='landing'),
    path('about/', views.about, name='about'),
    path('transactions/', views.transaction_index, name="transaction-index"),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/signin/', views.Signin.as_view(), name='signin'),
    path('profile/', views.profile, name='profile'),
    path('addmoney/', views.add_money, name='add-money')
]

