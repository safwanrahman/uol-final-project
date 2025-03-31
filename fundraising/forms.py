from django import forms
from .models import FundraisingPost, Transaction

class FundraisingPostForm(forms.ModelForm):
    class Meta:
        model = FundraisingPost
        fields = ['title', 'description', 'target_amount', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class DonationForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        } 