from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail


@shared_task(name="send welcome email task E_commerce")
def send_welcome_email_eco(subject, message, from_email, to):
    try:
        send_mail(subject, message, from_email, to)
        print(f"sent successfully to {to}")
    except:
        print(f"error while sending email to {to}")  
    return "EXECUTED"    
