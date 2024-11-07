from django.urls import path
from . import views 

urlpatterns = [
    path('', views.landing, name='landing'),
    path('about/', views.about, name='about'),
    path('transactions/', views.transaction_index, name='transaction-index'),
    path('transactions/<int:transaction_id>/', views.transaction_detail, name='transaction-detail'),
    path('transactions/<int:transaction_id>/add_comment/', views.add_comment, name='add-comment'),
    path('transactions/<int:transaction_id>/remove-comment/<int:comment_id>/', views.remove_comment, name='remove-comment'),
    path('transactions/<int:transaction_id>/update-note', views.update_note, name='update-note'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/signin/', views.Signin.as_view(), name='signin'),
    path('profile/', views.profile, name='profile'),
    path('addmoney/', views.add_money, name='add-money'),
    path('sendmoney/', views.TransactionCreate.as_view(), name='transaction-create')
]

