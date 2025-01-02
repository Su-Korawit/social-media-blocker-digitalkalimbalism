from django import forms
from .models import User, Progress

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
    
class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['description', 'progress_percentage']  # ฟิลด์ที่ต้องการในฟอร์ม
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'รายละเอียด'}),
            'progress_percentage': forms.NumberInput(attrs={'step': 0.01, 'placeholder': 'เปอร์เซ็นต์ความคืบหน้า'}),
        }