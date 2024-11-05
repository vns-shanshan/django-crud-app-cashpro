from decimal import Decimal
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Transaction, Profile
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q




# class Transaction:
#     def __init__(self, sender, receiver, amount, note, created_at):
#         self.sender = sender
#         self.receiver = receiver
#         self.amount = amount
#         self.note = note
#         self.created_at = created_at

# transactions = [
#     Transaction('Vanessa', 'Ryan', 5.00, 'Happy Halloween!', '11/01/24'),
#     Transaction('Amy', 'Bryan', 10.00, 'Split the pizza.', '10/31/24'),
#     Transaction('Cathy', 'Dylan', 15.00, 'Coffee run for the team.', '10/30/24'),
#     Transaction('Eric', 'Frank', 20.00, 'Movie tickets.', '10/29/24')
# ]
        
# Create your views here.
def landing(request):
    return render(request, 'landing.html')

def about(request):
    return render(request, 'about.html')

def transaction_index(request):
    transactions = Transaction.objects.all()
    return render(request, 'transactions/index.html', {'transactions': transactions})

@login_required
def profile(request):
    profile_from_db = Profile.objects.get(user_id=request.user.id)

    profile = request.user.profile
    transactions = Transaction.objects.filter(Q(sender=profile) | Q(receiver=profile))
    
    return render(request, 'profile.html', {'profile': profile_from_db, 'transactions': transactions})

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            Profile.objects.create(user=user)

            login(request, user)
            return redirect('profile')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

class Signin(LoginView):
    template_name = 'signin.html'
    next_page = "profile"

    # def get_success_url(self):
    #     # Ensure the user is authenticated before retrieving user_id
    #     user_id = self.request.user.id if self.request.user.is_authenticated else None
    #     if user_id:
    #         return reverse('profile', kwargs={'user_id': user_id})
    #     else:
    #         return reverse('signin')  # Redirect to signin if user_id is None

@login_required
def add_money(request):
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))
        profile = Profile.objects.get(user_id=request.user.id)

        new_balance = profile.balance + amount
        profile.balance = new_balance

        profile.save()
        return redirect('profile')
    return render(request, 'add_money.html')