# forms.py
from django import forms
from django.contrib.auth import get_user_model

from .models import Drone

User = get_user_model()


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'phone_number']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DroneForm(forms.ModelForm):
    class Meta:
        model = Drone
        fields = ['drone_model', 'drone_sn', 'remote_sn', 'workspace_id', 'status']
        widgets = {
            'drone_model': forms.Select(attrs={'class': 'form-control'}),
            'drone_sn': forms.TextInput(attrs={'class': 'form-control'}),
            'remote_sn': forms.TextInput(attrs={'class': 'form-control'}),
            'workspace_id': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
