from django.db import models
from django.contrib.auth.models import User
from core.models import Service
from phonenumber_field.modelfields import PhoneNumberField
from .utils import send_appointment_approved_msg

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    phone = PhoneNumberField()
    is_active = models.BooleanField(default=True)
    services_offered = models.ManyToManyField(Service, blank=True)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('REJECTED', 'Rejected'),
    ]

    TYPE_CHOICES = [
        ('PARLOUR', 'At Parlour'),
        ('HOME', 'At Home'),
    ]

    customer_name = models.CharField(max_length=100)
    customer_phone = PhoneNumberField()
    customer_email = models.EmailField(blank=True)
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    
    date = models.DateField()
    time_slot = models.TimeField()
    
    appointment_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='PARLOUR')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    
    address = models.TextField(blank=True, null=True, help_text="Required for Home Services")
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    
    admin_notes = models.TextField(blank=True, help_text="Private logic for staff")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Calculate price
        if not self.total_price:
            if self.appointment_type == 'HOME' and self.service.is_home_service_available:
                self.total_price = self.service.home_price or self.service.parlour_price
            else:
                self.total_price = self.service.parlour_price
        
        # Check for status change to APPROVED
        is_approval = False
        if self.pk:
            try:
                old_instance = Appointment.objects.get(pk=self.pk)
                if old_instance.status != 'APPROVED' and self.status == 'APPROVED':
                    is_approval = True
            except Appointment.DoesNotExist:
                pass

        super().save(*args, **kwargs)

        if is_approval:
            try:
                send_appointment_approved_msg(self)
            except Exception as e:
                print(f"Error sending approval msg: {e}")

    def __str__(self):
        return f"{self.customer_name} - {self.service.name} ({self.date})"
