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
    subject = models.CharField(max_length=191, verbose_name="Sujet")
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
        ('archived', 'Archivé'),
    ]

    subject = models.CharField(max_length=191, verbose_name="Sujet")
    body_html = models.TextField(verbose_name="Contenu HTML")
    body_text = models.TextField(blank=True, verbose_name="Contenu texte")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sent_emails')
    recipients = models.ManyToManyField(User, related_name='received_emails')
    cc = models.ManyToManyField(User, related_name='cc_emails', blank=True)
    bcc = models.ManyToManyField(User, related_name='bcc_emails', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Statut")
    is_read = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)
    is_important = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name="Date d'envoi")
    template = models.ForeignKey('EmailTemplate', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('mails:email_detail', kwargs={'pk': self.pk})

    def send(self):
        """Envoie l'email"""
        if self.is_sent:
            return False

        try:
            # Préparer les destinataires
            recipients = list(self.recipients.all()) + list(self.cc.all()) + list(self.bcc.all())

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
            self.is_sent = True
            self.sent_at = timezone.now()
            self.save()

            return True
        except Exception as e:
            self.status = 'failed'
            self.is_sent = False
            self.error_message = str(e)
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

class Folder(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    description = models.TextField(blank=True, verbose_name="Description")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='email_folders', verbose_name="Utilisateur")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name="Dossier parent")

    class Meta:
        verbose_name = "Dossier"
        verbose_name_plural = "Dossiers"
        ordering = ['name']
        unique_together = ['name', 'user', 'parent']

    def __str__(self):
        return self.name

class Contact(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    company = models.CharField(max_length=100, blank=True, verbose_name="Entreprise")
    notes = models.TextField(blank=True, verbose_name="Notes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contacts', verbose_name="Utilisateur")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    groups = models.ManyToManyField('ContactGroup', blank=True, related_name='contacts', verbose_name="Groupes")

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ['last_name', 'first_name']
        unique_together = ['email', 'user']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class ContactGroup(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    description = models.TextField(blank=True, verbose_name="Description")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contact_groups', verbose_name="Utilisateur")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")

    class Meta:
        verbose_name = "Groupe de contacts"
        verbose_name_plural = "Groupes de contacts"
        ordering = ['name']
        unique_together = ['name', 'user']

    def __str__(self):
        return self.name
