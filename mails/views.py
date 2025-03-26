from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Email, EmailTemplate, EmailAttachment, Folder, Contact, ContactGroup
from .forms import EmailForm, EmailTemplateForm, FolderForm, ContactForm, ContactGroupForm
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
        Q(recipients=request.user)
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
            Q(recipients__email__icontains=search) |
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

@login_required
def folder_list(request):
    folders = Folder.objects.filter(user=request.user)
    context = {
        'folders': folders,
    }
    return render(request, 'mails/folder_list.html', context)

@login_required
def folder_create(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user
            folder.save()
            messages.success(request, 'Dossier créé avec succès.')
            return redirect('mails:folder_list')
    else:
        form = FolderForm()
    
    context = {
        'form': form,
    }
    return render(request, 'mails/folder_form.html', context)

@login_required
def folder_detail(request, pk):
    folder = get_object_or_404(Folder, pk=pk, user=request.user)
    emails = folder.emails.all()
    context = {
        'folder': folder,
        'emails': emails,
    }
    return render(request, 'mails/folder_detail.html', context)

@login_required
def folder_edit(request, pk):
    folder = get_object_or_404(Folder, pk=pk, user=request.user)
    if request.method == 'POST':
        form = FolderForm(request.POST, instance=folder)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dossier mis à jour avec succès.')
            return redirect('mails:folder_list')
    else:
        form = FolderForm(instance=folder)
    
    context = {
        'form': form,
        'folder': folder,
    }
    return render(request, 'mails/folder_form.html', context)

@login_required
@require_POST
def folder_delete(request, pk):
    folder = get_object_or_404(Folder, pk=pk, user=request.user)
    folder.delete()
    messages.success(request, 'Dossier supprimé avec succès.')
    return redirect('mails:folder_list')

@login_required
def contact_list(request):
    contacts = Contact.objects.filter(user=request.user)
    context = {
        'contacts': contacts,
    }
    return render(request, 'mails/contact_list.html', context)

@login_required
def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            messages.success(request, 'Contact créé avec succès.')
            return redirect('mails:contact_list')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'mails/contact_form.html', context)

@login_required
def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    context = {
        'contact': contact,
    }
    return render(request, 'mails/contact_detail.html', context)

@login_required
def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact mis à jour avec succès.')
            return redirect('mails:contact_list')
    else:
        form = ContactForm(instance=contact)
    
    context = {
        'form': form,
        'contact': contact,
    }
    return render(request, 'mails/contact_form.html', context)

@login_required
@require_POST
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    contact.delete()
    messages.success(request, 'Contact supprimé avec succès.')
    return redirect('mails:contact_list')

@login_required
def contact_import(request):
    if request.method == 'POST':
        # TODO: Implement contact import functionality
        messages.success(request, 'Contacts importés avec succès.')
        return redirect('mails:contact_list')
    return render(request, 'mails/contact_import.html')

@login_required
def group_list(request):
    groups = ContactGroup.objects.filter(user=request.user)
    context = {
        'groups': groups,
    }
    return render(request, 'mails/group_list.html', context)

@login_required
def group_create(request):
    if request.method == 'POST':
        form = ContactGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.user = request.user
            group.save()
            messages.success(request, 'Groupe créé avec succès.')
            return redirect('mails:groups')
    else:
        form = ContactGroupForm()
    
    context = {
        'form': form,
    }
    return render(request, 'mails/group_form.html', context)

@login_required
def group_detail(request, pk):
    group = get_object_or_404(ContactGroup, pk=pk, user=request.user)
    context = {
        'group': group,
    }
    return render(request, 'mails/group_detail.html', context)

@login_required
def group_edit(request, pk):
    group = get_object_or_404(ContactGroup, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ContactGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, 'Groupe mis à jour avec succès.')
            return redirect('mails:groups')
    else:
        form = ContactGroupForm(instance=group)
    
    context = {
        'form': form,
        'group': group,
    }
    return render(request, 'mails/group_form.html', context)

@login_required
@require_POST
def group_delete(request, pk):
    group = get_object_or_404(ContactGroup, pk=pk, user=request.user)
    group.delete()
    messages.success(request, 'Groupe supprimé avec succès.')
    return redirect('mails:groups')

@login_required
def email_search(request):
    query = request.GET.get('q', '')
    emails = Email.objects.filter(
        Q(sender=request.user) | 
        Q(recipient_email=request.user.email)
    ).filter(
        Q(subject__icontains=query) |
        Q(body_text__icontains=query) |
        Q(recipient_email__icontains=query)
    ).order_by('-created_at')
    
    context = {
        'emails': emails,
        'query': query,
    }
    return render(request, 'mails/email_search.html', context)

@login_required
def email_settings(request):
    if request.method == 'POST':
        # TODO: Implement email settings functionality
        messages.success(request, 'Paramètres mis à jour avec succès.')
        return redirect('mails:email_settings')
    return render(request, 'mails/email_settings.html')

@login_required
def email_archive(request):
    emails = Email.objects.filter(
        Q(sender=request.user) | 
        Q(recipient_email=request.user.email)
    ).filter(
        status='ARCHIVED'
    ).order_by('-created_at')
    
    context = {
        'emails': emails,
    }
    return render(request, 'mails/email_archive.html', context)
