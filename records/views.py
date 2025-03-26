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
    ReferenceValue
)
from .serializers import (
    FolderSerializer, FolderDetailSerializer, MetadataDefinitionSerializer,
    DocumentMetadataSerializer, FolderMetadataSerializer, ReferenceListSerializer,
    ReferenceValueSerializer, DocumentSerializer
)
from django.http import FileResponse

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

class DocumentDetailView(LoginRequiredMixin, DetailView):
    model = Document
    template_name = 'records/document_detail.html'
    context_object_name = 'document'

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
