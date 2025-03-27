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
from django.db.models import Q

class CorrespondenceListView(LoginRequiredMixin, ListView):
    model = Correspondence
    template_name = 'correspondence/correspondences/correspondence_list.html'
    context_object_name = 'correspondences'

    def get_queryset(self):
        return Correspondence.objects.filter(
            sender_user=self.request.user
        ) | Correspondence.objects.filter(
            recipient_user=self.request.user
        ).order_by('-date')

class IncomingCorrespondenceListView(LoginRequiredMixin, ListView):
    model = Correspondence
    template_name = 'correspondence/correspondences/correspondence_list.html'
    context_object_name = 'correspondences'

    def get_queryset(self):
        return Correspondence.objects.filter(
            recipient_user=self.request.user,
            document_type='incoming'
        ).order_by('-date')

class OutgoingCorrespondenceListView(LoginRequiredMixin, ListView):
    model = Correspondence
    template_name = 'correspondence/correspondences/correspondence_list.html'
    context_object_name = 'correspondences'

    def get_queryset(self):
        return Correspondence.objects.filter(
            sender_user=self.request.user,
            document_type='outgoing'
        ).order_by('-date')

class InternalCorrespondenceListView(LoginRequiredMixin, ListView):
    model = Correspondence
    template_name = 'correspondence/correspondences/correspondence_list.html'
    context_object_name = 'correspondences'

    def get_queryset(self):
        return Correspondence.objects.filter(
            sender_user=self.request.user,
            document_type='internal'
        ).order_by('-date')

class RecentCorrespondenceListView(LoginRequiredMixin, ListView):
    model = Correspondence
    template_name = 'correspondence/correspondences/correspondence_list.html'
    context_object_name = 'correspondences'

    def get_queryset(self):
        return (Correspondence.objects.filter(
            sender_user=self.request.user
        ) | Correspondence.objects.filter(
            recipient_user=self.request.user
        )).order_by('-date')[:50]

class FavoritesCorrespondenceListView(LoginRequiredMixin, ListView):
    model = Correspondence
    template_name = 'correspondence/correspondences/correspondence_list.html'
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
    template_name = 'correspondence/correspondences/correspondence_detail.html'
    context_object_name = 'correspondence'

    def get_queryset(self):
        queryset = Correspondence.objects.all()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(sender_user=self.request.user) | queryset.filter(recipient_user=self.request.user)

class CorrespondenceCreateView(LoginRequiredMixin, CreateView):
    model = Correspondence
    template_name = 'correspondence/correspondences/correspondence_form.html'
    fields = ['code', 'name', 'date', 'description', 'document_type', 'status', 
              'priority', 'typology', 'action', 'recipient_user', 'recipient_organisation']
    success_url = reverse_lazy('correspondence:list')

    def form_valid(self, form):
        form.instance.sender_user = self.request.user
        form.instance.sender_organisation = self.request.user.organisation
        return super().form_valid(form)

class CorrespondenceUpdateView(LoginRequiredMixin, UpdateView):
    model = Correspondence
    template_name = 'correspondence/correspondences/correspondence_form.html'
    fields = ['code', 'name', 'date', 'description', 'document_type', 'status', 
              'priority', 'typology', 'action', 'recipient_user', 'recipient_organisation']
    success_url = reverse_lazy('correspondence:list')

class CorrespondenceDeleteView(LoginRequiredMixin, DeleteView):
    model = Correspondence
    template_name = 'correspondence/correspondences/correspondence_confirm_delete.html'
    success_url = reverse_lazy('correspondence:list')

@login_required
def correspondence_archive(request, pk):
    correspondence = get_object_or_404(Correspondence, pk=pk)
    correspondence.is_archived = True
    correspondence.save()
    messages.success(request, 'Correspondence archived successfully.')
    return redirect('correspondence:list')

# Batch Views
class CorrespondenceBatchListView(LoginRequiredMixin, ListView):
    model = Batch
    template_name = 'correspondence/batches/batch_list.html'
    context_object_name = 'batches'

    def get_queryset(self):
        return Batch.objects.all()

class CorrespondenceBatchDetailView(LoginRequiredMixin, DetailView):
    model = Batch
    template_name = 'correspondence/batches/batch_detail.html'
    context_object_name = 'batch'

    def get_queryset(self):
        return Batch.objects.all()

class CorrespondenceBatchCreateView(LoginRequiredMixin, CreateView):
    model = Batch
    template_name = 'correspondence/batches/batch_form.html'
    fields = ['code', 'name', 'organisation_holder']
    success_url = reverse_lazy('correspondence:batch_list')

    def form_valid(self, form):
        return super().form_valid(form)

class CorrespondenceBatchUpdateView(LoginRequiredMixin, UpdateView):
    model = Batch
    template_name = 'correspondence/batches/batch_form.html'
    fields = ['code', 'name', 'organisation_holder']
    success_url = reverse_lazy('correspondence:batch_list')

class CorrespondenceBatchDeleteView(LoginRequiredMixin, DeleteView):
    model = Batch
    template_name = 'correspondence/batches/batch_confirm_delete.html'
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
    return render(request, 'templates/scan.html', context)

# Folder Views
class CorrespondenceFolderListView(LoginRequiredMixin, ListView):
    model = CorrespondenceFolder
    template_name = 'correspondence/folders/folder_list.html'
    context_object_name = 'folders'

    def get_queryset(self):
        return CorrespondenceFolder.objects.filter(
            Q(created_by=self.request.user) | Q(shared_with=self.request.user)
        ).distinct()

class CorrespondenceFolderDetailView(LoginRequiredMixin, DetailView):
    model = CorrespondenceFolder
    template_name = 'correspondence/folders/folder_detail.html'
    context_object_name = 'folder'

    def get_queryset(self):
        return CorrespondenceFolder.objects.filter(
            Q(created_by=self.request.user) | Q(shared_with=self.request.user)
        )

class CorrespondenceFolderCreateView(LoginRequiredMixin, CreateView):
    model = CorrespondenceFolder
    template_name = 'correspondence/folders/folder_form.html'
    fields = ['name', 'description', 'parent', 'shared_with']
    success_url = reverse_lazy('correspondence:folder_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class CorrespondenceFolderUpdateView(LoginRequiredMixin, UpdateView):
    model = CorrespondenceFolder
    template_name = 'correspondence/folders/folder_form.html'
    fields = ['name', 'description', 'parent', 'shared_with']
    success_url = reverse_lazy('correspondence:folder_list')

class CorrespondenceFolderDeleteView(LoginRequiredMixin, DeleteView):
    model = CorrespondenceFolder
    template_name = 'correspondence/folders/folder_confirm_delete.html'
    success_url = reverse_lazy('correspondence:folder_list')

# Template Views
class CorrespondenceTemplateListView(LoginRequiredMixin, ListView):
    model = CorrespondenceTemplate
    template_name = 'correspondence/templates/template_list.html'
    context_object_name = 'templates'

    def get_queryset(self):
        return CorrespondenceTemplate.objects.filter(
            Q(created_by=self.request.user) | Q(shared_with=self.request.user)
        ).distinct()

class CorrespondenceTemplateDetailView(LoginRequiredMixin, DetailView):
    model = CorrespondenceTemplate
    template_name = 'correspondence/templates/template_detail.html'
    context_object_name = 'template'

    def get_queryset(self):
        return CorrespondenceTemplate.objects.filter(
            Q(created_by=self.request.user) | Q(shared_with=self.request.user)
        )

class CorrespondenceTemplateCreateView(LoginRequiredMixin, CreateView):
    model = CorrespondenceTemplate
    template_name = 'correspondence/templates/template_form.html'
    fields = ['name', 'description', 'content', 'document_type', 'shared_with']
    success_url = reverse_lazy('correspondence:template_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class CorrespondenceTemplateUpdateView(LoginRequiredMixin, UpdateView):
    model = CorrespondenceTemplate
    template_name = 'correspondence/templates/template_form.html'
    fields = ['name', 'description', 'content', 'document_type', 'shared_with']
    success_url = reverse_lazy('correspondence:template_list')

class CorrespondenceTemplateDeleteView(LoginRequiredMixin, DeleteView):
    model = CorrespondenceTemplate
    template_name = 'correspondence/templates/template_confirm_delete.html'
    success_url = reverse_lazy('correspondence:template_list')

class CorrespondenceAttachmentListView(LoginRequiredMixin, ListView):
    model = CorrespondenceAttachment
    template_name = 'correspondence/attachments/attachment_list.html'
    context_object_name = 'attachments'

    def get_queryset(self):
        return CorrespondenceAttachment.objects.filter(
            correspondence__sender_user=self.request.user
        ) | CorrespondenceAttachment.objects.filter(
            correspondence__recipient_user=self.request.user
        ).distinct()

class CorrespondenceAttachmentDetailView(LoginRequiredMixin, DetailView):
    model = CorrespondenceAttachment
    template_name = 'correspondence/attachments/attachment_detail.html'
    context_object_name = 'attachment'

    def get_queryset(self):
        return CorrespondenceAttachment.objects.filter(
            correspondence__sender_user=self.request.user
        ) | CorrespondenceAttachment.objects.filter(
            correspondence__recipient_user=self.request.user
        )

class CorrespondenceAttachmentCreateView(LoginRequiredMixin, CreateView):
    model = CorrespondenceAttachment
    template_name = 'correspondence/attachments/attachment_form.html'
    fields = ['correspondence', 'file', 'name', 'description']
    success_url = reverse_lazy('correspondence:attachment_list')

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)

class CorrespondenceAttachmentUpdateView(LoginRequiredMixin, UpdateView):
    model = CorrespondenceAttachment
    template_name = 'correspondence/attachments/attachment_form.html'
    fields = ['correspondence', 'file', 'name', 'description']
    success_url = reverse_lazy('correspondence:attachment_list')

class CorrespondenceAttachmentDeleteView(LoginRequiredMixin, DeleteView):
    model = CorrespondenceAttachment
    template_name = 'correspondence/attachments/attachment_confirm_delete.html'
    success_url = reverse_lazy('correspondence:attachment_list')

class CorrespondenceRelatedListView(LoginRequiredMixin, ListView):
    model = CorrespondenceRelated
    template_name = 'correspondence/related/related_list.html'
    context_object_name = 'related_correspondences'

    def get_queryset(self):
        return CorrespondenceRelated.objects.filter(
            correspondence__sender_user=self.request.user
        ) | CorrespondenceRelated.objects.filter(
            correspondence__recipient_user=self.request.user
        ).distinct()

class CorrespondenceRelatedDetailView(LoginRequiredMixin, DetailView):
    model = CorrespondenceRelated
    template_name = 'correspondence/related/related_detail.html'
    context_object_name = 'related_correspondence'

    def get_queryset(self):
        return CorrespondenceRelated.objects.filter(
            correspondence__sender_user=self.request.user
        ) | CorrespondenceRelated.objects.filter(
            correspondence__recipient_user=self.request.user
        )

class CorrespondenceRelatedCreateView(LoginRequiredMixin, CreateView):
    model = CorrespondenceRelated
    template_name = 'correspondence/related/related_form.html'
    fields = ['correspondence', 'related_correspondence', 'relation_type']
    success_url = reverse_lazy('correspondence:related_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class CorrespondenceRelatedUpdateView(LoginRequiredMixin, UpdateView):
    model = CorrespondenceRelated
    template_name = 'correspondence/related/related_form.html'
    fields = ['correspondence', 'related_correspondence', 'relation_type']
    success_url = reverse_lazy('correspondence:related_list')

class CorrespondenceRelatedDeleteView(LoginRequiredMixin, DeleteView):
    model = CorrespondenceRelated
    template_name = 'correspondence/related/related_confirm_delete.html'
    success_url = reverse_lazy('correspondence:related_list')

class CorrespondencePriorityListView(LoginRequiredMixin, ListView):
    model = CorrespondencePriority
    template_name = 'correspondence/priorities/priority_list.html'
    context_object_name = 'priorities'

    def get_queryset(self):
        return CorrespondencePriority.objects.filter(
            created_by=self.request.user
        ).order_by('name')

class CorrespondencePriorityDetailView(LoginRequiredMixin, DetailView):
    model = CorrespondencePriority
    template_name = 'correspondence/priorities/priority_detail.html'
    context_object_name = 'priority'

    def get_queryset(self):
        return CorrespondencePriority.objects.filter(
            created_by=self.request.user
        )

class CorrespondencePriorityCreateView(LoginRequiredMixin, CreateView):
    model = CorrespondencePriority
    template_name = 'correspondence/priorities/priority_form.html'
    fields = ['name', 'description', 'color']
    success_url = reverse_lazy('correspondence:priority_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class CorrespondencePriorityUpdateView(LoginRequiredMixin, UpdateView):
    model = CorrespondencePriority
    template_name = 'correspondence/priorities/priority_form.html'
    fields = ['name', 'description', 'color']
    success_url = reverse_lazy('correspondence:priority_list')

class CorrespondencePriorityDeleteView(LoginRequiredMixin, DeleteView):
    model = CorrespondencePriority
    template_name = 'correspondence/priorities/priority_confirm_delete.html'
    success_url = reverse_lazy('correspondence:priority_list')

class CorrespondenceTypologyListView(LoginRequiredMixin, ListView):
    model = CorrespondenceTypology
    template_name = 'correspondence/typologies/typology_list.html'
    context_object_name = 'typologies'

    def get_queryset(self):
        return CorrespondenceTypology.objects.filter(
            created_by=self.request.user
        ).order_by('name')

class CorrespondenceTypologyDetailView(LoginRequiredMixin, DetailView):
    model = CorrespondenceTypology
    template_name = 'correspondence/typologies/typology_detail.html'
    context_object_name = 'typology'

    def get_queryset(self):
        return CorrespondenceTypology.objects.filter(
            created_by=self.request.user
        )

class CorrespondenceTypologyCreateView(LoginRequiredMixin, CreateView):
    model = CorrespondenceTypology
    template_name = 'correspondence/typologies/typology_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('correspondence:typology_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class CorrespondenceTypologyUpdateView(LoginRequiredMixin, UpdateView):
    model = CorrespondenceTypology
    template_name = 'correspondence/typologies/typology_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('correspondence:typology_list')

class CorrespondenceTypologyDeleteView(LoginRequiredMixin, DeleteView):
    model = CorrespondenceTypology
    template_name = 'correspondence/typologies/typology_confirm_delete.html'
    success_url = reverse_lazy('correspondence:typology_list')

class CorrespondenceActionListView(LoginRequiredMixin, ListView):
    model = CorrespondenceAction
    template_name = 'correspondence/actions/action_list.html'
    context_object_name = 'actions'

    def get_queryset(self):
        return CorrespondenceAction.objects.filter(
            created_by=self.request.user
        ).order_by('name')

class CorrespondenceActionDetailView(LoginRequiredMixin, DetailView):
    model = CorrespondenceAction
    template_name = 'correspondence/actions/action_detail.html'
    context_object_name = 'action'

    def get_queryset(self):
        return CorrespondenceAction.objects.filter(
            created_by=self.request.user
        )

class CorrespondenceActionCreateView(LoginRequiredMixin, CreateView):
    model = CorrespondenceAction
    template_name = 'correspondence/actions/action_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('correspondence:action_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class CorrespondenceActionUpdateView(LoginRequiredMixin, UpdateView):
    model = CorrespondenceAction
    template_name = 'correspondence/actions/action_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('correspondence:action_list')

class CorrespondenceActionDeleteView(LoginRequiredMixin, DeleteView):
    model = CorrespondenceAction
    template_name = 'correspondence/actions/action_confirm_delete.html'
    success_url = reverse_lazy('correspondence:action_list') 