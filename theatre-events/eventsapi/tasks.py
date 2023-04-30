from celery import shared_task
from django.core.mail import send_mail

from main import settings


@shared_task()
def send_email(subject, message, recipient_list, html_content):
    from_email = settings.EMAIL_HOST_USER
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_content,
        fail_silently=False,
    )
