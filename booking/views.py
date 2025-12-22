import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from .models import Appointment, Staff
from .forms import AppointmentForm
from core.models import Service

# from .utils import send_whatsapp_notification

def book_appointment(request):
    if request.method == 'POST':
        print("\n\n=== NEW APPOINTMENT SUBMISSION ===")
        print("POST Data:", request.POST)
        form = AppointmentForm(request.POST)
        if form.is_valid():
            print("Form is VALID. Saving...")
            appt = form.save(commit=False)
            
            # Simple overlap check can be added here or rely on admin/constraint
            # appt.full_clean() # Optional
            
            appt.save()
            
            # Send Notification
            # try:
            #     send_whatsapp_notification(appt)
            # except Exception as e:
            #     print(f"Notification failed: {e}")
            
            messages.success(request, 'Appointment requested successfully! We will confirm shortly.')
            return redirect('home')
        else:
            print("Form Errors:", form.errors) # Debugging Code
            messages.error(request, 'Please correct the errors below.')
    else:
        initial = {}
        if 'service_id' in request.GET:
            initial['service'] = request.GET.get('service_id')
        form = AppointmentForm(initial=initial)

    return render(request, 'booking/book.html', {'form': form}) 

def get_available_slots(request):
    date_str = request.GET.get('date')
    service_id = request.GET.get('service_id')
    
    if not date_str or not service_id:
        return JsonResponse({'slots': []})
        
    try:
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        service = Service.objects.get(id=service_id)
    except:
        return JsonResponse({'slots': []})

    # Logic: 10:00 to 20:00
    # Create slots based on duration
    # Exclude slots that overlap with existing appointments
    
    slots = []
    start_hour = 10
    end_hour = 20
    
    current_time = datetime.datetime.combine(date_obj, datetime.time(start_hour, 0))
    close_time = datetime.datetime.combine(date_obj, datetime.time(end_hour, 0))
    
    duration = datetime.timedelta(minutes=service.duration_minutes)
    
    # Existing appointments for that day
    appointments = Appointment.objects.filter(date=date_obj, status__in=['PENDING', 'APPROVED'])
    
    while current_time + duration <= close_time:
        slot_start = current_time
        slot_end = current_time + duration
        
        # Check collision
        is_taken = False
        for appt in appointments:
            appt_start = datetime.datetime.combine(date_obj, appt.time_slot)
            appt_end = appt_start + datetime.timedelta(minutes=appt.service.duration_minutes)
            
            # Overlap: (StartA < EndB) and (EndA > StartB)
            if slot_start < appt_end and slot_end > appt_start:
                is_taken = True
                break
        
        if not is_taken:
            slots.append(slot_start.strftime('%H:%M'))
            
        current_time += datetime.timedelta(minutes=30) # 30 min interval options
        
    return JsonResponse({'slots': slots, 'home_price': service.home_price, 'parlour_price': service.parlour_price})
