from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
import os
import mimetypes
import uuid

User = get_user_model()

class EmailTemplate(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    subject = models.CharField(max_length=200, verbose_name="Sujet")
    body_html = models.TextField(verbose_name="Contenu HTML")
    body_text = models.TextField(blank=True, verbose_name="Contenu texte")
    variables = models.TextField(blank=True, help_text="Liste des variables disponibles (une par ligne)", verbose_name="Variables")
    category = models.CharField(max_length=50, blank=True, verbose_name="Catégorie")
    is_system = models.BooleanField(default=False, verbose_name="Template système")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_templates', verbose_name="Créé par")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_templates', verbose_name="Modifié par")

    class Meta:
        verbose_name = "Template d'email"
        verbose_name_plural = "Templates d'emails"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('mails:template_edit', kwargs={'pk': self.pk})

    def clean(self):
        if self.is_system and self.pk:
            # Vérifier si le template système est modifié
            original = EmailTemplate.objects.get(pk=self.pk)
            if original.is_system and (
                self.subject != original.subject or
                self.body_html != original.body_html or
                self.body_text != original.body_text
            ):
                raise ValidationError("Les templates système ne peuvent pas être modifiés.")

class Email(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('pending', 'En attente'),
        ('sent', 'Envoyé'),
        ('failed', 'Échec'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Basse'),
        ('normal', 'Normale'),
        ('high', 'Haute'),
        ('urgent', 'Urgente'),
    ]

    recipient_email = models.EmailField(verbose_name="Email du destinataire")
    recipient_name = models.CharField(max_length=100, blank=True, verbose_name="Nom du destinataire")
    cc = models.TextField(blank=True, help_text="Adresses email séparées par des virgules", verbose_name="Copie carbone")
    bcc = models.TextField(blank=True, help_text="Adresses email séparées par des virgules", verbose_name="Copie carbone cachée")
    subject = models.CharField(max_length=200, verbose_name="Sujet")
    body_html = models.TextField(verbose_name="Contenu HTML")
    body_text = models.TextField(blank=True, verbose_name="Contenu texte")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal', verbose_name="Priorité")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="Statut")
    template = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Template")
    related_entity_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Type d'entité liée")
    related_entity_id = models.PositiveIntegerField(null=True, blank=True, verbose_name="ID de l'entité liée")
    related_entity = GenericForeignKey('related_entity_type', 'related_entity_id')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name="Date d'envoi")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='sent_emails', verbose_name="Expéditeur")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_emails', verbose_name="Créé par")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_emails', verbose_name="Modifié par")

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {self.recipient_email}"

    def get_absolute_url(self):
        return reverse('mails:email_detail', kwargs={'pk': self.pk})

    def send(self):
        """Envoie l'email"""
        if self.status == 'sent':
            return False

        try:
            # Préparer les destinataires
            recipients = [self.recipient_email]
            if self.cc:
                recipients.extend([email.strip() for email in self.cc.split(',')])

            # Préparer le contenu HTML
            html_content = render_to_string('mails/email_template.html', {
                'email': self,
                'attachments': self.attachments.all()
            })

            # Préparer le contenu texte
            text_content = render_to_string('mails/email_template.txt', {
                'email': self,
                'attachments': self.attachments.all()
            })

            # Envoyer l'email
            send_mail(
                subject=self.subject,
                message=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipients,
                html_message=html_content,
                fail_silently=False,
            )

            # Mettre à jour le statut
            self.status = 'sent'
            self.sent_at = timezone.now()
            self.save()

            return True
        except Exception as e:
            self.status = 'failed'
            self.save()
            raise e

class EmailAttachment(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE, related_name='attachments', verbose_name="Email")
    file = models.FileField(upload_to='email_attachments/%Y/%m/%d/', verbose_name="Fichier")
    filename = models.CharField(max_length=255, verbose_name="Nom du fichier")
    mime_type = models.CharField(max_length=100, blank=True, verbose_name="Type MIME")
    file_size = models.PositiveIntegerField(verbose_name="Taille du fichier")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        verbose_name = "Pièce jointe"
        verbose_name_plural = "Pièces jointes"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.filename} ({self.email.subject})"

    def save(self, *args, **kwargs):
        if not self.mime_type:
            self.mime_type = mimetypes.guess_type(self.filename)[0] or 'application/octet-stream'
        if not self.file_size and self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('mails:download_attachment', kwargs={
            'email_id': self.email.pk,
            'attachment_id': self.pk
        })
