from django.core.management.base import BaseCommand
from scheduling.models import Pabellon

class Command(BaseCommand):
    help = 'Crea los pabellones iniciales'

    def handle(self, *args, **kwargs):
        pabellones = [
            # Pabellones de cirugía mayor
            {'nombre': f'Pabellón Mayor {i}', 'tipo': 'CIRUGIA_MAYOR'} for i in range(1, 15)
        ] + [
            {'nombre': f'Pabellón Mayor Complejo {i}', 'tipo': 'CIRUGIA_MAYOR_COMPLEJA'} for i in range(1, 3)
        ] + [
            # Pabellones de maternidad - ginecología
            {'nombre': f'Pabellón Maternidad/Ginecología {i}', 'tipo': 'MATERNIDAD_GINECOLOGIA'} for i in range(1, 9)
        ] + [
            # Pabellones de cirugía ambulatoria
            {'nombre': f'Pabellón Cirugía Ambulatoria {i}', 'tipo': 'CIRUGIA_AMBULATORIA'} for i in range(1, 7)
        ] + [
            # Pabellón de hemodinamia
            {'nombre': 'Pabellón Hemodinamia', 'tipo': 'HEMODINAMIA'}
        ]

        for pabellon_data in pabellones:
            Pabellon.objects.get_or_create(**pabellon_data)

        self.stdout.write(self.style.SUCCESS('Pabellones creados exitosamente.'))