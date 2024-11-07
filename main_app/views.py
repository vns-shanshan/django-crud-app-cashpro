from decimal import Decimal
import random
from django.shortcuts import render, redirect
from .models import Transaction, Profile, Comment
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from .form import CommentForm, TransactionForm, UpdateNoteForm
from django.shortcuts import get_object_or_404
        
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

@login_required
def transaction_detail(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)

    comment_form = CommentForm()
    
    return render(request, 'transactions/detail.html', {'transaction': transaction, 'comment_form': comment_form})

@login_required
def add_comment(request, transaction_id):
    form = CommentForm(request.POST)

    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.transaction_id = transaction_id
        new_comment.user_id = request.user.id
        new_comment.save()

    return redirect('transaction-detail', transaction_id=transaction_id)

@login_required
def remove_comment(request, transaction_id, comment_id):

    to_delete = get_object_or_404(Comment, id=comment_id)

    if request.user.id == to_delete.user.id:
        to_delete.delete()
    return redirect('transaction-detail', transaction_id=transaction_id)

@login_required
def update_note(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    
    if request.method == "POST":
        form = UpdateNoteForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()  
            return redirect('transaction-detail', transaction_id=transaction_id)
    else:
        form = UpdateNoteForm(instance=transaction)

    return render(request, 'transactions/update_note.html', {'update_note_form': form, 'transaction_id': transaction_id})

class TransactionCreate(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class= TransactionForm
    success_url = '/profile/'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields['receiver'].widget = forms.TextInput(attrs={'placeholder': 'Enter Username'})

        return form
    
    def form_valid(self, form):
        form.instance.sender = self.request.user.profile 
        sender_user_id = self.request.user.id
        receiver_user_id = form.instance.receiver.user_id
    
        try:
            if sender_user_id == receiver_user_id:
                raise ValueError("You cannot send money to yourself!")
            
            sender_profile_data = Profile.objects.get(user_id=sender_user_id)
            sender_profile_data.balance -= form.instance.amount
            sender_profile_data.save()

            receiver_profile_data = Profile.objects.get(user_id=receiver_user_id)
            receiver_profile_data.balance += form.instance.amount
            receiver_profile_data.save()

            return super().form_valid(form)
        
        except ValueError as e:
            form.add_error(None, str(e))  
            return self.form_invalid(form) 

        

