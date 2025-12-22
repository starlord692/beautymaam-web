import os
# from twilio.rest import Client  # Removed for production readiness
from django.conf import settings

def send_appointment_approved_msg(appointment):
    """
    Stub for sending real WhatsApp/SMS approval message.
    Disabled for production deployment to avoid external dependencies.
    """
    print(f"STUB: Sending approval message to {appointment.customer_name} ({appointment.customer_phone})")
    return
