from django import forms
from .models import fighter_profile
from django.contrib.auth.models import User

class user_registration_form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput,label="confirm password")
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    
class fighter_profile_form(forms.ModelForm):
    class Meta:
        model = fighter_profile
        fields = ['age', 'gender', 'height', 'weight', 'selected_fighting_style', 'learning_level']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'selected_fighting_style': forms.Select(attrs={'class': 'form-control'}),
            'learning_level': forms.Select(attrs={'class': 'form-control'}),
        }