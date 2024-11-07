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
        
        # Attempt to retrieve the user by username
        try:
            receiver_user = User.objects.get(username=receiver_username)

        except User.DoesNotExist:
            raise forms.ValidationError("User with this username does not exist.")
        
        # Return the user’s profile or ID if that's what the field expects
        return receiver_user.profile  # or `receiver_user.id` if `receiver` is a ForeignKey to `User`
    
class UpdateNoteForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['note']