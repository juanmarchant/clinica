from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('NURSE', 'Nurse'),
        ('DOCTOR', 'Doctor'),
        ('AUXILIAR', 'Auxiliar'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Pabellon(models.Model):
    ESTADO_CHOICES = [
        ('OCUPADO', 'Ocupado'),
        ('DESOCUPADO', 'Desocupado'),
        ('LIMPIEZA', 'Limpieza'),
    ]
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='DESOCUPADO')

    def __str__(self):
        return self.nombre

class Schedule(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'DOCTOR'}, related_name='doctor_schedules')
    auxiliar = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'AUXILIAR'}, related_name='auxiliar_schedules')
    pabellon = models.ForeignKey(Pabellon, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()

