
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Schedule, Pabellon
from django.contrib.auth import authenticate, login
from .forms import CustomLoginForm, ScheduleForm
from django.http import JsonResponse
from datetime import datetime, timedelta

@login_required
def view_schedule(request):
    if request.user.role == 'DOCTOR':
        schedules = Schedule.objects.filter(doctor=request.user)
    else:
        schedules = None
    return render(request, 'scheduling/view_schedule.html', {'schedules': schedules})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('create_schedule')
    else:
        form = CustomLoginForm()
    return render(request, 'scheduling/login.html', {'form': form})

@login_required
def create_schedule(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            # Marcar el pabellón como ocupado
            pabellon = form.cleaned_data['pabellon']
            pabellon.estado = 'OCUPADO'
            pabellon.save()
            form.save()
            return redirect('schedule_success')
    else:
        form = ScheduleForm()

    return render(request, 'scheduling/create_schedule.html', {'form': form})



def schedule_success(request):
    return render(request, 'scheduling/schedule_success.html')


# Vista para mostrar el calendario
def calendar_view(request):
    return render(request, 'scheduling/calendar.html')

# Vista para obtener los agendamientos en formato JSON para FullCalendar
def get_schedule_events(request):
    events = Schedule.objects.all()
    event_list = []

    for event in events:
        # Combina la fecha y hora para el inicio del evento
        start_time = datetime.combine(event.date, event.time)
        # Asume que el evento dura una hora, si es necesario ajusta este valor
        end_time = start_time + timedelta(hours=1)

        event_list.append({
            'title': event.description,
            'start': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'description': event.description,
            'id': event.id,
            'surgeon': event.surgeon.username,
            'anesthetist': event.anesthetist.username,
        })

    return JsonResponse(event_list, safe=False)

def schedule_list(request):
    schedules = Schedule.objects.all()
    pabellones = Pabellon.objects.all()
    return render(request, 'scheduling/schedule_list.html', {'schedules': schedules, 'pabellones': pabellones})