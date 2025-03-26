from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Correspondence, CorrespondencePriority, CorrespondenceTypology, CorrespondenceAction, CorrespondenceAttachment, CorrespondenceRelated, Batch, BatchCorrespondence, BatchTransaction, CorrespondenceFolder, CorrespondenceTemplate
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
import csv
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from .forms import CorrespondenceForm, BatchForm, CorrespondenceFolderForm, CorrespondenceTemplateForm

class CorrespondenceListView(LoginRequiredMixin, ListView):
    model = Correspondence
    template_name = 'correspondence/correspondence_list.html'
    context_object_name = 'correspondences'

    def get_queryset(self):
        return Correspondence.objects.filter(
            sender_user=self.request.user
        ) | Correspondence.objects.filter(
            recipient_user=self.request.user
        ).order_by('-date')

class IncomingCorrespondenceListView(LoginRequiredMixin, ListView):
    model = Correspondence
    template_name = 'correspondence/correspondence_list.html'
    context_object_name = 'correspondences'

    def get_queryset(self):
        return Correspondence.objects.filter(
            recipient_user=self.request.user,
            document_type='incoming'
        ).order_by('-date')

class OutgoingCorrespondenceListView(LoginRequiredMixin, ListView):
    model = Correspondence
    template_name = 'correspondence/correspondence_list.html'
    context_object_name = 'correspondences'

    def get_queryset(self):
        return Correspondence.objects.filter(
            sender_user=self.request.user,
            document_type='outgoing'
        ).order_by('-date')

class InternalCorrespondenceListView(LoginRequiredMixin, ListView):
    model = Correspondence
    template_name = 'correspondence/correspondence_list.html'
    context_object_name = 'correspondences'

    def get_queryset(self):
        return Correspondence.objects.filter(
            sender_user=self.request.user,
            document_type='internal'
        ).order_by('-date')

class RecentCorrespondenceListView(LoginRequiredMixin, ListView):
    model = Correspondence
    template_name = 'correspondence/correspondence_list.html'
    context_object_name = 'correspondences'

    def get_queryset(self):
        return (Correspondence.objects.filter(
            sender_user=self.request.user
        ) | Correspondence.objects.filter(
            recipient_user=self.request.user
        )).order_by('-date')[:50]

class FavoritesCorrespondenceListView(LoginRequiredMixin, ListView):
    model = Correspondence
    template_name = 'correspondence/correspondence_list.html'
    context_object_name = 'correspondences'

    def get_queryset(self):
        return (Correspondence.objects.filter(
            sender_user=self.request.user,
            is_favorite=True
        ) | Correspondence.objects.filter(
            recipient_user=self.request.user,
            is_favorite=True
        )).order_by('-date')

class CorrespondenceDetailView(LoginRequiredMixin, DetailView):
    model = Correspondence
    template_name = 'correspondence/correspondence_detail.html'
    context_object_name = 'correspondence'

    def get_queryset(self):
        queryset = Correspondence.objects.all()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(sender_user=self.request.user) | queryset.filter(recipient_user=self.request.user)

class CorrespondenceCreateView(LoginRequiredMixin, CreateView):
    model = Correspondence
    template_name = 'correspondence/correspondence_form.html'
    fields = ['code', 'name', 'date', 'description', 'document_type', 'status', 
              'priority', 'typology', 'action', 'recipient_user', 'recipient_organisation']
    success_url = reverse_lazy('correspondence:list')

    def form_valid(self, form):
        form.instance.sender_user = self.request.user
        form.instance.sender_organisation = self.request.user.organisation
        return super().form_valid(form)

class CorrespondenceUpdateView(LoginRequiredMixin, UpdateView):
    model = Correspondence
    template_name = 'correspondence/correspondence_form.html'
    fields = ['code', 'name', 'date', 'description', 'document_type', 'status', 
              'priority', 'typology', 'action', 'recipient_user', 'recipient_organisation']
    success_url = reverse_lazy('correspondence:list')

class CorrespondenceDeleteView(LoginRequiredMixin, DeleteView):
    model = Correspondence
    template_name = 'correspondence/correspondence_confirm_delete.html'
    success_url = reverse_lazy('correspondence:list')

@login_required
def correspondence_archive(request, pk):
    correspondence = get_object_or_404(Correspondence, pk=pk)
    correspondence.is_archived = True
    correspondence.save()
    messages.success(request, 'Correspondence archived successfully.')
    return redirect('correspondence:list')

# Batch Views
class BatchListView(LoginRequiredMixin, ListView):
    model = Batch
    template_name = 'correspondence/batch_list.html'
    context_object_name = 'batches'

class BatchDetailView(LoginRequiredMixin, DetailView):
    model = Batch
    template_name = 'correspondence/batch_detail.html'
    context_object_name = 'batch'

class BatchCreateView(LoginRequiredMixin, CreateView):
    model = Batch
    template_name = 'correspondence/batch_form.html'
    fields = ['code', 'name', 'organisation_holder']
    success_url = reverse_lazy('correspondence:batch_list')

class BatchUpdateView(LoginRequiredMixin, UpdateView):
    model = Batch
    template_name = 'correspondence/batch_form.html'
    fields = ['code', 'name', 'organisation_holder']
    success_url = reverse_lazy('correspondence:batch_list')

class BatchDeleteView(LoginRequiredMixin, DeleteView):
    model = Batch
    template_name = 'correspondence/batch_confirm_delete.html'
    success_url = reverse_lazy('correspondence:batch_list')

@login_required
def add_correspondence_to_batch(request, batch_pk, correspondence_pk):
    batch = get_object_or_404(Batch, pk=batch_pk)
    correspondence = get_object_or_404(Correspondence, pk=correspondence_pk)
    
    BatchCorrespondence.objects.create(
        batch=batch,
        correspondence=correspondence,
        insert_by=request.user,
        insert_by_organisation=request.user.organisation
    )
    messages.success(request, 'Correspondence added to batch successfully.')
    return redirect('correspondence:batch_detail', pk=batch_pk)

@login_required
def remove_correspondence_from_batch(request, batch_pk, correspondence_pk):
    batch_correspondence = get_object_or_404(BatchCorrespondence, batch_id=batch_pk, correspondence_id=correspondence_pk)
    batch_correspondence.remove_date = timezone.now()
    batch_correspondence.remove_by = request.user
    batch_correspondence.remove_by_organisation = request.user.organisation
    batch_correspondence.save()
    messages.success(request, 'Correspondence removed from batch successfully.')
    return redirect('correspondence:batch_detail', pk=batch_pk)

@login_required
def export_data(request):
    """Export correspondence data in CSV format."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="correspondence_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Subject', 'Status', 'Created By', 'Created At', 'Updated At'])
    
    # Export correspondence
    correspondences = Correspondence.objects.all()
    for correspondence in correspondences:
        writer.writerow([
            correspondence.subject,
            correspondence.status,
            correspondence.created_by.get_full_name(),
            correspondence.created_at,
            correspondence.updated_at
        ])
    
    return response

@login_required
def scan(request):
    """Vue pour la numérisation de documents"""
    if request.method == 'POST':
        # TODO: Implémenter le traitement du formulaire
        messages.success(request, 'Document numérisé avec succès')
        return redirect('correspondence:list')
    
    context = {
        'priorities': CorrespondencePriority.objects.all(),
    }
    return render(request, 'correspondence/scan.html', context)

# Folder Views
class FolderListView(LoginRequiredMixin, ListView):
    model = CorrespondenceFolder
    template_name = 'correspondence/folder_list.html'
    context_object_name = 'folders'

    def get_queryset(self):
        return CorrespondenceFolder.objects.filter(
            created_by=self.request.user
        ).order_by('name')

class FolderCreateView(LoginRequiredMixin, CreateView):
    model = CorrespondenceFolder
    template_name = 'correspondence/folder_form.html'
    form_class = CorrespondenceFolderForm
    success_url = reverse_lazy('correspondence:folder_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class FolderUpdateView(LoginRequiredMixin, UpdateView):
    model = CorrespondenceFolder
    template_name = 'correspondence/folder_form.html'
    form_class = CorrespondenceFolderForm
    success_url = reverse_lazy('correspondence:folder_list')

class FolderDeleteView(LoginRequiredMixin, DeleteView):
    model = CorrespondenceFolder
    template_name = 'correspondence/folder_confirm_delete.html'
    success_url = reverse_lazy('correspondence:folder_list')

class FolderDetailView(LoginRequiredMixin, DetailView):
    model = CorrespondenceFolder
    template_name = 'correspondence/folder_detail.html'
    context_object_name = 'folder'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['correspondences'] = Correspondence.objects.filter(
            folder=self.object
        ).order_by('-date')
        return context 

# Template Views
class TemplateListView(LoginRequiredMixin, ListView):
    model = CorrespondenceTemplate
    template_name = 'correspondence/template_list.html'
    context_object_name = 'templates'

    def get_queryset(self):
        return CorrespondenceTemplate.objects.filter(
            created_by=self.request.user
        ).order_by('name')

class TemplateCreateView(LoginRequiredMixin, CreateView):
    model = CorrespondenceTemplate
    template_name = 'correspondence/template_form.html'
    form_class = CorrespondenceTemplateForm
    success_url = reverse_lazy('correspondence:template_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class TemplateUpdateView(LoginRequiredMixin, UpdateView):
    model = CorrespondenceTemplate
    template_name = 'correspondence/template_form.html'
    form_class = CorrespondenceTemplateForm
    success_url = reverse_lazy('correspondence:template_list')

class TemplateDeleteView(LoginRequiredMixin, DeleteView):
    model = CorrespondenceTemplate
    template_name = 'correspondence/template_confirm_delete.html'
    success_url = reverse_lazy('correspondence:template_list')

class TemplateDetailView(LoginRequiredMixin, DetailView):
    model = CorrespondenceTemplate
    template_name = 'correspondence/template_detail.html'
    context_object_name = 'template' 