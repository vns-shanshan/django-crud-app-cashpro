from django import forms
from .models import Comment, Transaction, User

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class TransactionForm(forms.ModelForm):
    receiver = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}))

    class Meta:
        model = Transaction
        fields = ['receiver', 'amount', 'note']

    def clean_receiver(self):
        receiver_username = self.cleaned_data.get('receiver')
        
        try:
            receiver_user = User.objects.get(username=receiver_username)

        except User.DoesNotExist:
            raise forms.ValidationError("User with this username does not exist.")
        
        return receiver_user.profile  
    
class UpdateNoteForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['note']