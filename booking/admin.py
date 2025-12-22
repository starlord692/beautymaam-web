from django.contrib import admin
from .models import Staff, Appointment

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'is_active')
    filter_horizontal = ('services_offered',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'service', 'date', 'time_slot', 'status', 'staff', 'appointment_type')
    list_filter = ('status', 'date', 'appointment_type', 'staff')
    search_fields = ('customer_name', 'customer_phone')
    date_hierarchy = 'date'
    list_editable = ('status', 'staff')
    
    fieldsets = (
        ('Customer Info', {
            'fields': ('customer_name', 'customer_phone', 'customer_email', 'address')
        }),
        ('Booking Details', {
            'fields': ('service', 'date', 'time_slot', 'appointment_type', 'total_price')
        }),
        ('Status & Staff', {
            'fields': ('status', 'staff', 'admin_notes')
        }),
    )
    readonly_fields = ('total_price', 'created_at')
