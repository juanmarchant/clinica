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
    class Meta:
        model = Schedule
        fields = [
            'patient_name', 'surgeon', 'anesthetist', 'nurse', 
            'arsenero', 'pabellonero', 'tecnico_anestesia', 
            'pabellon', 'date', 'time', 'description'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_pabellon(self):
        pabellon = self.cleaned_data['pabellon']
        if pabellon.estado != 'DESOCUPADO':
            raise forms.ValidationError(f"El pabellón {pabellon.nombre} no está disponible.")
        return pabellon