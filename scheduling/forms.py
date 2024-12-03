from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Schedule, User


class CustomLoginForm(AuthenticationForm):
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Invalid username or password.")
        if user.role != 'NURSE':
            raise forms.ValidationError("Only Nurses are allowed to log in.")
        return cleaned_data

class ScheduleForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(
        queryset=User.objects.filter(role='DOCTOR'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Assigned Doctor",
    )

    auxiliar = forms.ModelChoiceField(
        queryset=User.objects.filter(role='AUXILIAR'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Assigned Auxiliar",
    )

    class Meta:
        model = Schedule
        fields = ['doctor','auxiliar','pabellon' ,'date', 'time', 'description']
        widgets = {
            'date': forms.Select(attrs={ 'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

