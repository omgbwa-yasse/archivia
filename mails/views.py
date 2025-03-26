from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Email, EmailTemplate, EmailAttachment
from .forms import EmailForm, EmailTemplateForm
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.urls import reverse
from celery import shared_task
import os

@login_required
def email_list(request):
    emails = Email.objects.filter(
        Q(sender=request.user) | 
        Q(recipient_email=request.user.email)
    ).order_by('-created_at')
    
    # Filtrage
    status = request.GET.get('status')
    if status:
        emails = emails.filter(status=status)
    
    # Recherche
    search = request.GET.get('search')
    if search:
        emails = emails.filter(
            Q(subject__icontains=search) |
            Q(recipient_email__icontains=search) |
            Q(body_text__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(emails, 20)
    page = request.GET.get('page')
    emails = paginator.get_page(page)
    
    context = {
        'emails': emails,
        'status_choices': Email.STATUS_CHOICES,
    }
    return render(request, 'mails/email_list.html', context)

@login_required
def email_detail(request, pk):
    email = get_object_or_404(Email, pk=pk)
    
    # Vérifier les permissions
    if email.sender != request.user and email.recipient_email != request.user.email:
        messages.error(request, "Vous n'avez pas accès à cet email.")
        return redirect('mails:email_list')
    
    context = {
        'email': email,
    }
    return render(request, 'mails/email_detail.html', context)

@login_required
def create_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.save(commit=False)
            email.sender = request.user
            email.save()
            
            # Gérer les pièces jointes multiples
            attachments = request.FILES.getlist('attachments')
            for attachment in attachments:
                # Sauvegarder le fichier
                file_path = default_storage.save(f'email_attachments/{email.id}/{attachment.name}', attachment)
                
                # Créer l'objet EmailAttachment
                EmailAttachment.objects.create(
                    email=email,
                    file=file_path,
                    filename=attachment.name
                )
            
            # Envoyer l'email de manière asynchrone
            send_email_task.delay(email.id)
            
            messages.success(request, 'Email créé avec succès et en cours d\'envoi.')
            return redirect('mails:email_detail', pk=email.pk)
    else:
        form = EmailForm()
    
    context = {
        'form': form,
        'templates': EmailTemplate.objects.all(),
    }
    return render(request, 'mails/email_form.html', context)

@login_required
def edit_email(request, pk):
    email = get_object_or_404(Email, pk=pk)
    
    # Vérifier les permissions
    if email.sender != request.user:
        messages.error(request, "Vous ne pouvez pas modifier cet email.")
        return redirect('mails:email_detail', pk=pk)
    
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES, instance=email)
        if form.is_valid():
            email = form.save()
            
            # Gérer les nouvelles pièces jointes
            attachments = request.FILES.getlist('attachments')
            for attachment in attachments:
                file_path = default_storage.save(f'email_attachments/{email.id}/{attachment.name}', attachment)
                EmailAttachment.objects.create(
                    email=email,
                    file=file_path,
                    filename=attachment.name
                )
            
            messages.success(request, 'Email mis à jour avec succès.')
            return redirect('mails:email_detail', pk=email.pk)
    else:
        form = EmailForm(instance=email)
    
    context = {
        'form': form,
        'email': email,
        'templates': EmailTemplate.objects.all(),
    }
    return render(request, 'mails/email_form.html', context)

@login_required
@require_POST
def email_delete(request, pk):
    email = get_object_or_404(Email, pk=pk)
    
    # Vérifier les permissions
    if email.sender != request.user:
        messages.error(request, "Vous ne pouvez pas supprimer cet email.")
        return redirect('mails:email_detail', pk=pk)
    
    email.delete()
    messages.success(request, "L'email a été supprimé avec succès.")
    return redirect('mails:email_list')

@login_required
@require_POST
def email_send(request, pk):
    email = get_object_or_404(Email, pk=pk)
    
    # Vérifier les permissions
    if email.sender != request.user:
        messages.error(request, "Vous ne pouvez pas envoyer cet email.")
        return JsonResponse({'status': 'error'}, status=403)
    
    try:
        # TODO: Implémenter l'envoi d'email
        email.status = 'SENT'
        email.sent_at = timezone.now()
        email.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        email.status = 'FAILED'
        email.error_message = str(e)
        email.save()
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
def template_list(request):
    templates = EmailTemplate.objects.all().order_by('name')
    context = {
        'templates': templates,
    }
    return render(request, 'mails/template_list.html', context)

@login_required
def create_template(request):
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            template.created_by = request.user
            template.save()
            messages.success(request, "Le template a été créé avec succès.")
            return redirect('mails:template_list')
    else:
        form = EmailTemplateForm()
    
    context = {
        'form': form,
    }
    return render(request, 'mails/template_form.html', context)

@login_required
def edit_template(request, pk):
    template = get_object_or_404(EmailTemplate, pk=pk)
    
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST, instance=template)
        if form.is_valid():
            template = form.save(commit=False)
            template.updated_by = request.user
            template.save()
            messages.success(request, "Le template a été mis à jour avec succès.")
            return redirect('mails:template_list')
    else:
        form = EmailTemplateForm(instance=template)
    
    context = {
        'form': form,
        'template': template,
    }
    return render(request, 'mails/template_form.html', context)

@login_required
@require_POST
def template_delete(request, pk):
    template = get_object_or_404(EmailTemplate, pk=pk)
    
    if template.is_system:
        messages.error(request, "Vous ne pouvez pas supprimer un template système.")
        return redirect('mails:template_list')
    
    template.delete()
    messages.success(request, "Le template a été supprimé avec succès.")
    return redirect('mails:template_list')

@shared_task
def send_email_task(email_id):
    email = Email.objects.get(pk=email_id)
    
    # Préparer le contenu HTML
    html_content = render_to_string('mails/email_template.html', {
        'email': email,
        'attachments': email.attachments.all()
    })
    
    # Préparer le contenu texte
    text_content = render_to_string('mails/email_template.txt', {
        'email': email,
        'attachments': email.attachments.all()
    })
    
    # Envoyer l'email
    send_mail(
        subject=email.subject,
        message=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=email.recipients.split(','),
        html_message=html_content,
        fail_silently=False,
    )
    
    # Mettre à jour le statut de l'email
    email.status = 'sent'
    email.save()

@login_required
def download_attachment(request, email_id, attachment_id):
    email = get_object_or_404(Email, pk=email_id)
    attachment = get_object_or_404(EmailAttachment, pk=attachment_id, email=email)
    
    file_path = attachment.file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{attachment.filename}"'
            return response
    return HttpResponse(status=404)
