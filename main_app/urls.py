from django.urls import path
from . import views 

urlpatterns = [
    path('', views.landing, name='landing'),
    path('about/', views.about, name='about'),
    path('transactions/', views.transaction_index, name="transaction-index"),
    path('accounts/signup/', views.signup, name='signup')
]

