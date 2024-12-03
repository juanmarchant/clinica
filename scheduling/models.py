from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('NURSE', 'Nurse'),
        ('DOCTOR', 'Doctor'),
        ('AUXILIAR', 'Auxiliar'),
        ('ARSENALERO', 'Arsenalero/a'),
        ('PABELLONERO', 'Pabellonero/a'),
        ('TECNICO_ANESTESIA', 'Técnico/a de Anestesia'),
        ('ANESTESISTA', 'Anestesista'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class Pabellon(models.Model):
    TIPO_CHOICES = [
        ('CIRUGIA_MAYOR', 'Cirugía Mayor'),
        ('CIRUGIA_MAYOR_COMPLEJA', 'Cirugía Mayor Compleja'),
        ('MATERNIDAD_GINECOLOGIA', 'Maternidad/Ginecología'),
        ('CIRUGIA_AMBULATORIA', 'Cirugía Ambulatoria'),
        ('HEMODINAMIA', 'Hemodinamia'),
    ]
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    estado = models.CharField(
        max_length=10,
        choices=[
            ('OCUPADO', 'Ocupado'),
            ('DESOCUPADO', 'Desocupado'),
            ('LIMPIEZA', 'Limpieza'),
        ],
        default='DESOCUPADO'
    )

    def __str__(self):
        return self.nombre

class Schedule(models.Model):
    patient_name = models.CharField(max_length=200)
    surgeon = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='surgeon_schedules', limit_choices_to={'role': 'DOCTOR'}
    )
    anesthetist = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='anesthetist_schedules', limit_choices_to={'role': 'DOCTOR'}
    )
    nurse = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='nurse_schedules', limit_choices_to={'role': 'NURSE'}
    )
    arsenero = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='arsenero_schedules',
        null=True,
        blank=True,
        limit_choices_to={'role': 'ARSENALERO'}
    )
    pabellonero = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='pabellonero_schedules', null=True, blank=True, limit_choices_to={'role': 'PABELLONERO'}
    )
    tecnico_anestesia = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tecnico_anestesia_schedules', null=True, blank=True, limit_choices_to={'role': 'TECNICO_ANESTESIA'}
    )
    pabellon = models.ForeignKey(Pabellon, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()