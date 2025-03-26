from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import (
    Folder, Document, MetadataDefinition,
    DocumentMetadata, FolderMetadata, ReferenceList,
    ReferenceValue, Category, Archive, Retention, AuditLog, AccessLog
)
from .serializers import (
    FolderSerializer, FolderDetailSerializer, MetadataDefinitionSerializer,
    DocumentMetadataSerializer, FolderMetadataSerializer, ReferenceListSerializer,
    ReferenceValueSerializer, DocumentSerializer
)
from django.http import FileResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Q
import csv

# Create your views here.

# Vues pour les templates
class FolderListView(LoginRequiredMixin, ListView):
    model = Folder
    template_name = 'records/folder_list.html'
    context_object_name = 'folders'
    
    def get_queryset(self):
        return Folder.objects.filter(parent=None)

class FolderDetailView(LoginRequiredMixin, DetailView):
    model = Folder
    template_name = 'records/folder_detail.html'
    context_object_name = 'folder'

class FolderCreateView(LoginRequiredMixin, CreateView):
    model = Folder
    template_name = 'records/folder_form.html'
    fields = ['name', 'description', 'parent']
    success_url = reverse_lazy('records:folder_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class FolderUpdateView(LoginRequiredMixin, UpdateView):
    model = Folder
    template_name = 'records/folder_form.html'
    fields = ['name', 'description', 'parent']
    success_url = reverse_lazy('records:folder_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class FolderDeleteView(LoginRequiredMixin, DeleteView):
    model = Folder
    template_name = 'records/folder_confirm_delete.html'
    success_url = reverse_lazy('records:folder_list')

    def delete(self, request, *args, **kwargs):
        folder = self.get_object()
        folder.soft_delete(request.user)
        return super().delete(request, *args, **kwargs)

class FolderRestoreView(LoginRequiredMixin, View):
    def post(self, request, pk):
        folder = get_object_or_404(Folder, pk=pk)
        folder.restore()
        return redirect('records:folder_list')

class DocumentListView(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'records/document_list.html'
    context_object_name = 'documents'

class DocumentImportView(LoginRequiredMixin, View):
    template_name = 'records/document_import.html'

    def get(self, request):
        folders = Folder.objects.filter(deleted_at__isnull=True)
        return render(request, self.template_name, {'folders': folders})

    def post(self, request):
        try:
            files = request.FILES.getlist('files')
            folder_id = request.POST.get('folder')
            folder = get_object_or_404(Folder, id=folder_id) if folder_id else None

            for file in files:
                Document.objects.create(
                    name=file.name,
                    file=file,
                    folder=folder,
                    created_by=request.user
                )

            messages.success(request, f'{len(files)} document(s) importé(s) avec succès')
            return redirect('records:document_list')
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'import: {str(e)}')
            folders = Folder.objects.filter(deleted_at__isnull=True)
            return render(request, self.template_name, {'folders': folders})

class DocumentDetailView(LoginRequiredMixin, DetailView):
    model = Document
    template_name = 'records/document_detail.html'
    context_object_name = 'document'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Log the document access
        document = self.get_object()
        AccessLog.objects.create(
            document=document,
            user=request.user,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        return response

class DocumentCreateView(LoginRequiredMixin, CreateView):
    model = Document
    template_name = 'records/document_form.html'
    fields = ['name', 'description', 'file', 'folder']
    success_url = reverse_lazy('records:document_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class DocumentUpdateView(LoginRequiredMixin, UpdateView):
    model = Document
    template_name = 'records/document_form.html'
    fields = ['name', 'description', 'file', 'folder']
    success_url = reverse_lazy('records:document_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class DocumentDeleteView(LoginRequiredMixin, DeleteView):
    model = Document
    template_name = 'records/document_confirm_delete.html'
    success_url = reverse_lazy('records:document_list')

class DocumentDownloadView(LoginRequiredMixin, View):
    def get(self, request, pk):
        document = get_object_or_404(Document, pk=pk)
        response = FileResponse(document.file, as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{document.file.name}"'
        return response

class MetadataDefinitionListView(LoginRequiredMixin, ListView):
    model = MetadataDefinition
    template_name = 'records/metadata_definition_list.html'
    context_object_name = 'metadata_definitions'

class MetadataDefinitionCreateView(LoginRequiredMixin, CreateView):
    model = MetadataDefinition
    template_name = 'records/metadata_definition_form.html'
    fields = ['name', 'description', 'field_type', 'is_required', 'reference_list']
    success_url = reverse_lazy('records:metadata_definition_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class MetadataDefinitionDetailView(LoginRequiredMixin, DetailView):
    model = MetadataDefinition
    template_name = 'records/metadata_definition_detail.html'
    context_object_name = 'metadata_definition'

class MetadataDefinitionUpdateView(LoginRequiredMixin, UpdateView):
    model = MetadataDefinition
    template_name = 'records/metadata_definition_form.html'
    fields = ['name', 'description', 'field_type', 'is_required', 'reference_list']
    success_url = reverse_lazy('records:metadata_definition_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class MetadataDefinitionDeleteView(LoginRequiredMixin, DeleteView):
    model = MetadataDefinition
    template_name = 'records/metadata_definition_confirm_delete.html'
    success_url = reverse_lazy('records:metadata_definition_list')

    def delete(self, request, *args, **kwargs):
        metadata_definition = self.get_object()
        metadata_definition.soft_delete(request.user)
        return super().delete(request, *args, **kwargs)

class ReferenceListListView(LoginRequiredMixin, ListView):
    model = ReferenceList
    template_name = 'records/reference_list_list.html'
    context_object_name = 'reference_lists'

class ReferenceListCreateView(LoginRequiredMixin, CreateView):
    model = ReferenceList
    template_name = 'records/reference_list_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('records:reference_list_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ReferenceListDetailView(LoginRequiredMixin, DetailView):
    model = ReferenceList
    template_name = 'records/reference_list_detail.html'
    context_object_name = 'reference_list'

class ReferenceListUpdateView(LoginRequiredMixin, UpdateView):
    model = ReferenceList
    template_name = 'records/reference_list_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('records:reference_list_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class ReferenceListDeleteView(LoginRequiredMixin, DeleteView):
    model = ReferenceList
    template_name = 'records/reference_list_confirm_delete.html'
    success_url = reverse_lazy('records:reference_list_list')

    def delete(self, request, *args, **kwargs):
        reference_list = self.get_object()
        reference_list.soft_delete(request.user)
        return super().delete(request, *args, **kwargs)

class ReferenceValueCreateView(LoginRequiredMixin, CreateView):
    model = ReferenceValue
    template_name = 'records/reference_value_form.html'
    fields = ['value', 'description']
    success_url = reverse_lazy('records:reference_list_list')

    def form_valid(self, form):
        form.instance.reference_list_id = self.kwargs['list_id']
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ReferenceValueUpdateView(LoginRequiredMixin, UpdateView):
    model = ReferenceValue
    template_name = 'records/reference_value_form.html'
    fields = ['value', 'description']
    success_url = reverse_lazy('records:reference_list_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class ReferenceValueDeleteView(LoginRequiredMixin, DeleteView):
    model = ReferenceValue
    template_name = 'records/reference_value_confirm_delete.html'
    success_url = reverse_lazy('records:reference_list_list')

    def delete(self, request, *args, **kwargs):
        reference_value = self.get_object()
        reference_value.soft_delete(request.user)
        return super().delete(request, *args, **kwargs)

# Vues pour l'API REST
class FolderViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FolderDetailSerializer
        return FolderSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    @action(detail=True, methods=['post'])
    def delete(self, request, pk=None):
        folder = self.get_object()
        folder.soft_delete(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        folder = self.get_object()
        folder.restore()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class MetadataDefinitionViewSet(viewsets.ModelViewSet):
    queryset = MetadataDefinition.objects.all()
    serializer_class = MetadataDefinitionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class FolderMetadataViewSet(viewsets.ModelViewSet):
    serializer_class = FolderMetadataSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FolderMetadata.objects.filter(folder_id=self.kwargs['pk'])

    def perform_create(self, serializer):
        serializer.save(folder_id=self.kwargs['pk'])

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class ReferenceListViewSet(viewsets.ModelViewSet):
    queryset = ReferenceList.objects.all()
    serializer_class = ReferenceListSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class ReferenceValueViewSet(viewsets.ModelViewSet):
    queryset = ReferenceValue.objects.all()
    serializer_class = ReferenceValueSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class FolderChildrenView(generics.ListAPIView):
    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Folder.objects.filter(parent_id=self.kwargs['pk'])

class FolderTreeView(generics.RetrieveAPIView):
    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Folder.objects.all()

    def retrieve(self, request, *args, **kwargs):
        folder = self.get_object()
        tree = self._build_tree(folder)
        return Response(tree)

    def _build_tree(self, folder):
        serializer = self.get_serializer(folder)
        data = serializer.data
        children = Folder.objects.filter(parent=folder)
        if children.exists():
            data['children'] = [self._build_tree(child) for child in children]
        return data

class TrashView(LoginRequiredMixin, View):
    template_name = 'records/trash.html'

    def get(self, request):
        deleted_folders = Folder.objects.filter(deleted_at__isnull=False)
        deleted_documents = Document.objects.filter(deleted_at__isnull=False)
        deleted_metadata = MetadataDefinition.objects.filter(deleted_at__isnull=False)
        deleted_reference_lists = ReferenceList.objects.filter(deleted_at__isnull=False)
        
        context = {
            'deleted_folders': deleted_folders,
            'deleted_documents': deleted_documents,
            'deleted_metadata': deleted_metadata,
            'deleted_reference_lists': deleted_reference_lists,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        action = request.POST.get('action')
        item_type = request.POST.get('type')
        item_id = request.POST.get('id')

        if action == 'restore':
            if item_type == 'folder':
                item = get_object_or_404(Folder, id=item_id)
                item.restore()
            elif item_type == 'document':
                item = get_object_or_404(Document, id=item_id)
                item.restore()
            elif item_type == 'metadata':
                item = get_object_or_404(MetadataDefinition, id=item_id)
                item.restore()
            elif item_type == 'reference_list':
                item = get_object_or_404(ReferenceList, id=item_id)
                item.restore()
            messages.success(request, f'{item_type.title()} restauré avec succès')
        elif action == 'delete':
            if item_type == 'folder':
                item = get_object_or_404(Folder, id=item_id)
                item.hard_delete()
            elif item_type == 'document':
                item = get_object_or_404(Document, id=item_id)
                item.hard_delete()
            elif item_type == 'metadata':
                item = get_object_or_404(MetadataDefinition, id=item_id)
                item.hard_delete()
            elif item_type == 'reference_list':
                item = get_object_or_404(ReferenceList, id=item_id)
                item.hard_delete()
            messages.success(request, f'{item_type.title()} supprimé définitivement')

        return redirect('records:trash')

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'records/category_form.html'
    fields = ['name', 'description', 'parent']
    success_url = reverse_lazy('records:category_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'records/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.filter(parent=None)

class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'records/category_detail.html'
    context_object_name = 'category'

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = 'records/category_form.html'
    fields = ['name', 'description', 'parent']
    success_url = reverse_lazy('records:category_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'records/category_confirm_delete.html'
    success_url = reverse_lazy('records:category_list')

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        category.soft_delete(request.user)
        return super().delete(request, *args, **kwargs)

class CategoryImportView(LoginRequiredMixin, View):
    template_name = 'records/category_import.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            file = request.FILES.get('file')
            if not file:
                messages.error(request, 'Aucun fichier n\'a été sélectionné')
                return render(request, self.template_name)

            # Here you would implement the actual import logic
            # For example, reading a CSV file and creating categories
            messages.success(request, 'Catégories importées avec succès')
            return redirect('records:category_list')
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'import: {str(e)}')
            return render(request, self.template_name)

class ArchiveListView(LoginRequiredMixin, ListView):
    model = Archive
    template_name = 'records/archive_list.html'
    context_object_name = 'archives'

class ArchiveCreateView(LoginRequiredMixin, CreateView):
    model = Archive
    template_name = 'records/archive_form.html'
    fields = ['name', 'description', 'location', 'capacity']
    success_url = reverse_lazy('records:archive_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ArchiveDetailView(LoginRequiredMixin, DetailView):
    model = Archive
    template_name = 'records/archive_detail.html'
    context_object_name = 'archive'

class ArchiveUpdateView(LoginRequiredMixin, UpdateView):
    model = Archive
    template_name = 'records/archive_form.html'
    fields = ['name', 'description', 'location', 'capacity']
    success_url = reverse_lazy('records:archive_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class ArchiveDeleteView(LoginRequiredMixin, DeleteView):
    model = Archive
    template_name = 'records/archive_confirm_delete.html'
    success_url = reverse_lazy('records:archive_list')

    def delete(self, request, *args, **kwargs):
        archive = self.get_object()
        archive.soft_delete(request.user)
        return super().delete(request, *args, **kwargs)

class RetentionListView(LoginRequiredMixin, ListView):
    model = Retention
    template_name = 'records/retention_list.html'
    context_object_name = 'retentions'

class RetentionCreateView(LoginRequiredMixin, CreateView):
    model = Retention
    template_name = 'records/retention_form.html'
    fields = ['name', 'description', 'retention_period', 'retention_type']
    success_url = reverse_lazy('records:retention_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class RetentionDetailView(LoginRequiredMixin, DetailView):
    model = Retention
    template_name = 'records/retention_detail.html'
    context_object_name = 'retention'

class RetentionUpdateView(LoginRequiredMixin, UpdateView):
    model = Retention
    template_name = 'records/retention_form.html'
    fields = ['name', 'description', 'retention_period', 'retention_type']
    success_url = reverse_lazy('records:retention_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class RetentionDeleteView(LoginRequiredMixin, DeleteView):
    model = Retention
    template_name = 'records/retention_confirm_delete.html'
    success_url = reverse_lazy('records:retention_list')

    def delete(self, request, *args, **kwargs):
        retention = self.get_object()
        retention.soft_delete(request.user)
        return super().delete(request, *args, **kwargs)

@login_required
def recent_documents(request):
    """View for displaying recently accessed documents."""
    # Get documents with access logs
    recent_docs = Document.objects.filter(
        access_logs__user=request.user
    ).distinct().order_by('-access_logs__accessed_at')[:10]
    
    # If there are fewer than 10 documents with access logs, add recently created documents
    if recent_docs.count() < 10:
        remaining_count = 10 - recent_docs.count()
        recent_created = Document.objects.exclude(
            id__in=recent_docs.values_list('id', flat=True)
        ).order_by('-created_at')[:remaining_count]
        recent_docs = list(recent_docs) + list(recent_created)
    
    context = {
        'documents': recent_docs,
        'title': 'Documents récents'
    }
    return render(request, 'records/document_list.html', context)

@login_required
def favorite_documents(request):
    """View for displaying favorite documents."""
    favorite_docs = Document.objects.filter(
        favorites__user=request.user
    ).distinct()
    
    context = {
        'documents': favorite_docs,
        'title': 'Documents favoris'
    }
    return render(request, 'records/document_list.html', context)

class CategoryTreeView(LoginRequiredMixin, View):
    template_name = 'records/category_tree.html'

    def get(self, request):
        root_categories = Category.objects.filter(parent=None, deleted_at__isnull=True)
        context = {
            'root_categories': root_categories,
            'title': 'Arborescence des catégories'
        }
        return render(request, self.template_name, context)

class CategoryStatsView(LoginRequiredMixin, View):
    template_name = 'records/category_stats.html'

    def get(self, request):
        # Get all categories
        categories = Category.objects.filter(deleted_at__isnull=True)
        total_categories = categories.count()
        total_documents = Document.objects.filter(deleted_at__isnull=True).count()
        
        # Calculate average documents per category
        avg_documents = round(total_documents / total_categories, 1) if total_categories > 0 else 0.0
        
        # Count documents per category
        category_stats = []
        for category in categories:
            doc_count = Document.objects.filter(category=category, deleted_at__isnull=True).count()
            subcategory_count = Category.objects.filter(parent=category, deleted_at__isnull=True).count()
            
            category_stats.append({
                'category': category,
                'document_count': doc_count,
                'subcategory_count': subcategory_count
            })
        
        context = {
            'category_stats': category_stats,
            'total_categories': total_categories,
            'total_documents': total_documents,
            'avg_documents': avg_documents,
            'title': 'Statistiques des catégories'
        }
        return render(request, self.template_name, context)

class DisposalListView(LoginRequiredMixin, ListView):
    template_name = 'records/disposal_list.html'
    context_object_name = 'documents'

    def get_queryset(self):
        # Get documents that have reached their retention period
        return Document.objects.filter(
            deleted_at__isnull=True,
            retention__isnull=False,
            created_at__lte=models.F('retention__retention_period')
        ).select_related('retention', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Documents à éliminer'
        return context

class SearchView(LoginRequiredMixin, View):
    template_name = 'records/search.html'

    def get(self, request):
        # Get search parameters from query string
        query = request.GET.get('q', '')
        category_id = request.GET.get('category')
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        retention_id = request.GET.get('retention')
        
        # Start with all non-deleted documents
        documents = Document.objects.filter(deleted_at__isnull=True)
        
        # Apply filters if provided
        if query:
            documents = documents.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
        
        if category_id:
            documents = documents.filter(category_id=category_id)
            
        if date_from:
            documents = documents.filter(created_at__gte=date_from)
            
        if date_to:
            documents = documents.filter(created_at__lte=date_to)
            
        if retention_id:
            documents = documents.filter(retention_id=retention_id)
        
        # Get filter options
        categories = Category.objects.filter(deleted_at__isnull=True)
        retentions = Retention.objects.filter(deleted_at__isnull=True)
        
        context = {
            'documents': documents,
            'query': query,
            'category_id': category_id,
            'date_from': date_from,
            'date_to': date_to,
            'retention_id': retention_id,
            'categories': categories,
            'retentions': retentions,
            'title': 'Recherche avancée'
        }
        return render(request, self.template_name, context)

class AuditLogView(LoginRequiredMixin, ListView):
    template_name = 'records/audit_log.html'
    context_object_name = 'audit_logs'
    paginate_by = 20

    def get_queryset(self):
        # Get all audit logs, ordered by timestamp
        return AuditLog.objects.all().order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Journal d\'audit'
        return context

@login_required
def export_data(request):
    """Export records data in CSV format."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="records_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Description', 'Created By', 'Created At', 'Updated At'])
    
    # Export folders
    folders = Folder.objects.filter(deleted_at__isnull=True)
    for folder in folders:
        writer.writerow([
            folder.name,
            folder.description,
            folder.created_by.get_full_name(),
            folder.created_at,
            folder.updated_at
        ])
    
    # Export documents
    documents = Document.objects.all()
    for document in documents:
        writer.writerow([
            document.name,
            document.description,
            document.created_by.get_full_name(),
            document.created_at,
            document.updated_at
        ])
    
    return response

@login_required
def settings(request):
    """View for managing records app settings."""
    if request.method == 'POST':
        # Handle settings update
        messages.success(request, 'Paramètres mis à jour avec succès')
        return redirect('records:settings')
    
    return render(request, 'records/settings.html')
