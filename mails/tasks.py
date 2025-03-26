from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from .models import Email, EmailTemplate
import json
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_email_task(email_id):
    """
    Tâche Celery pour envoyer un email en arrière-plan.
    """
    try:
        email = Email.objects.get(id=email_id)
        
        # Préparer le contenu de l'email
        if email.template:
            # Rendre le template avec les variables
            variables = json.loads(email.template.variables) if email.template.variables else {}
            body_html = render_to_string('mails/templates/email_template.html', {
                'content': email.template.body_html,
                **variables
            })
            body_text = render_to_string('mails/templates/email_template.txt', {
                'content': email.template.body_text or '',
                **variables
            })
        else:
            body_html = email.body_html
            body_text = email.body_text

        # Envoyer l'email
        send_mail(
            subject=email.subject,
            message=body_text,
            from_email=f"{email.sender_name} <{email.sender_email}>" if email.sender_name else email.sender_email,
            recipient_list=[email.recipient_email],
            html_message=body_html,
            fail_silently=False,
        )

        # Mettre à jour le statut
        email.status = 'SENT'
        email.sent_at = timezone.now()
        email.save()

    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email {email_id}: {str(e)}")
        if email:
            email.status = 'FAILED'
            email.error_message = str(e)
            email.save()
        raise

@shared_task
def process_email_queue():
    """
    Tâche Celery pour traiter la file d'attente des emails.
    """
    # Récupérer les emails en attente
    pending_emails = Email.objects.filter(status='PENDING')
    
    # Envoyer chaque email en attente
    for email in pending_emails:
        send_email_task.delay(email.id) 