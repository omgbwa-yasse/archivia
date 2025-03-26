from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Correspondence, CorrespondencePriority, CorrespondenceTypology, CorrespondenceAction, CorrespondenceAttachment, CorrespondenceRelated, Batch, BatchCorrespondence, BatchTransaction
from django.utils import timezone

class CorrespondenceListView(LoginRequiredMixin, ListView):
    model = Correspondence
    template_name = 'correspondence/correspondence_list.html'
    context_object_name = 'correspondences'
    paginate_by = 10

    def get_queryset(self):
        queryset = Correspondence.objects.all()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(sender_user=self.request.user) | queryset.filter(recipient_user=self.request.user)

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