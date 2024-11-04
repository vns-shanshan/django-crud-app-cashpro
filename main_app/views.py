from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Transaction, Profile
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


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

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            Profile.objects.create(user=user)

            login(request, user)
            return redirect('transaction-index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)