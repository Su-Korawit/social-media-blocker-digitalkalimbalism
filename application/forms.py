from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'tel']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Username'}),
            'tel': forms.TextInput(attrs={'placeholder': 'Telephone'}),
        }
        
    def clean_tel(self):
        tel = self.cleaned_data.get('tel')
        if not tel.isdigit() or len(tel) != 10:
            raise forms.ValidationError("Invalid phone number. Must be 10 digits.")
        return tel