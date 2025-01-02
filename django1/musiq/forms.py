from django import forms
from .models import Account

class IconUploadForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['userIcon']