from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, FileResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.conf import settings
from ..models import Workspace, WorkspaceMember, WorkspaceFolder, WorkspaceDocument, WorkspaceDocumentVersion
import os
from datetime import datetime

@login_required
def document_list(request, workspace_pk, folder_pk):
    """List all documents in a folder."""
    workspace = get_object_or_404(Workspace, pk=workspace_pk)
    member = get_object_or_404(WorkspaceMember, workspace=workspace, user=request.user)
    folder = get_object_or_404(WorkspaceFolder, pk=folder_pk, workspace=workspace)
    
    documents = folder.documents.all()
    
    return render(request, 'workspace/document_list.html', {
        'workspace': workspace,
        'folder': folder,
        'documents': documents,
        'user_member': member
    })

@login_required
def document_upload(request, workspace_pk, folder_pk):
    """Upload a new document to the folder."""
    workspace = get_object_or_404(Workspace, pk=workspace_pk)
    member = get_object_or_404(WorkspaceMember, workspace=workspace, user=request.user)
    folder = get_object_or_404(WorkspaceFolder, pk=folder_pk, workspace=workspace)
    
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        
        for file in files:
            try:
                # Create document
                document = WorkspaceDocument.objects.create(
                    workspace=workspace,
                    folder=folder,
                    name=file.name,
                    file_type=file.content_type,
                    file_size=file.size,
                    created_by=request.user
                )
                
                # Create initial version
                version = WorkspaceDocumentVersion.objects.create(
                    document=document,
                    version_number=1,
                    file=file,
                    created_by=request.user
                )
                
                messages.success(request, f'Document "{file.name}" has been uploaded.')
            except Exception as e:
                messages.error(request, f'Error uploading "{file.name}": {str(e)}')
    
    return redirect('workspace:document_list', workspace_pk=workspace_pk, folder_pk=folder_pk)

@login_required
def document_detail(request, workspace_pk, folder_pk, pk):
    """View document details and versions."""
    workspace = get_object_or_404(Workspace, pk=workspace_pk)
    member = get_object_or_404(WorkspaceMember, workspace=workspace, user=request.user)
    folder = get_object_or_404(WorkspaceFolder, pk=folder_pk, workspace=workspace)
    document = get_object_or_404(WorkspaceDocument, pk=pk, workspace=workspace, folder=folder)
    
    versions = document.versions.all().order_by('-version_number')
    
    return render(request, 'workspace/document_detail.html', {
        'workspace': workspace,
        'folder': folder,
        'document': document,
        'versions': versions,
        'user_member': member
    })

@login_required
def document_edit(request, workspace_pk, folder_pk, pk):
    """Edit document details or upload a new version."""
    workspace = get_object_or_404(Workspace, pk=workspace_pk)
    member = get_object_or_404(WorkspaceMember, workspace=workspace, user=request.user)
    folder = get_object_or_404(WorkspaceFolder, pk=folder_pk, workspace=workspace)
    document = get_object_or_404(WorkspaceDocument, pk=pk, workspace=workspace, folder=folder)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        new_file = request.FILES.get('file')
        
        try:
            document.name = name
            document.description = description
            document.updated_by = request.user
            document.save()
            
            if new_file:
                # Create new version
                version = WorkspaceDocumentVersion.objects.create(
                    document=document,
                    version_number=document.versions.count() + 1,
                    file=new_file,
                    created_by=request.user
                )
                
                document.file_type = new_file.content_type
                document.file_size = new_file.size
                document.save()
            
            messages.success(request, f'Document "{name}" has been updated.')
            return redirect('workspace:document_detail', workspace_pk=workspace_pk, folder_pk=folder_pk, pk=pk)
        except Exception as e:
            messages.error(request, str(e))
    
    return render(request, 'workspace/document_form.html', {
        'workspace': workspace,
        'folder': folder,
        'document': document,
        'user_member': member
    })

@login_required
@require_http_methods(["POST"])
def document_delete(request, workspace_pk, folder_pk, pk):
    """Delete a document and all its versions."""
    workspace = get_object_or_404(Workspace, pk=workspace_pk)
    member = get_object_or_404(WorkspaceMember, workspace=workspace, user=request.user)
    folder = get_object_or_404(WorkspaceFolder, pk=folder_pk, workspace=workspace)
    document = get_object_or_404(WorkspaceDocument, pk=pk, workspace=workspace, folder=folder)
    
    try:
        name = document.name
        document.delete()
        messages.success(request, f'Document "{name}" has been deleted.')
    except Exception as e:
        messages.error(request, str(e))
    
    return redirect('workspace:document_list', workspace_pk=workspace_pk, folder_pk=folder_pk)

@login_required
def document_download(request, workspace_pk, folder_pk, pk):
    """Download a specific version of a document."""
    workspace = get_object_or_404(Workspace, pk=workspace_pk)
    member = get_object_or_404(WorkspaceMember, workspace=workspace, user=request.user)
    folder = get_object_or_404(WorkspaceFolder, pk=folder_pk, workspace=workspace)
    document = get_object_or_404(WorkspaceDocument, pk=pk, workspace=workspace, folder=folder)
    
    version_id = request.GET.get('version')
    if version_id:
        version = get_object_or_404(WorkspaceDocumentVersion, pk=version_id, document=document)
    else:
        version = document.versions.latest('version_number')
    
    response = FileResponse(version.file)
    response['Content-Disposition'] = f'attachment; filename="{document.name}"'
    return response

@login_required
def document_share(request, workspace_pk, folder_pk, pk):
    """Share a document with other workspace members."""
    workspace = get_object_or_404(Workspace, pk=workspace_pk)
    member = get_object_or_404(WorkspaceMember, workspace=workspace, user=request.user)
    folder = get_object_or_404(WorkspaceFolder, pk=folder_pk, workspace=workspace)
    document = get_object_or_404(WorkspaceDocument, pk=pk, workspace=workspace, folder=folder)
    
    if request.method == 'POST':
        # Implement sharing logic here
        pass
    
    return render(request, 'workspace/document_share.html', {
        'workspace': workspace,
        'folder': folder,
        'document': document,
        'user_member': member
    })

@login_required
def document_versions(request, workspace_pk, folder_pk, pk):
    """View and manage document versions."""
    workspace = get_object_or_404(Workspace, pk=workspace_pk)
    member = get_object_or_404(WorkspaceMember, workspace=workspace, user=request.user)
    folder = get_object_or_404(WorkspaceFolder, pk=folder_pk, workspace=workspace)
    document = get_object_or_404(WorkspaceDocument, pk=pk, workspace=workspace, folder=folder)
    
    versions = document.versions.all().order_by('-version_number')
    
    return render(request, 'workspace/document_versions.html', {
        'workspace': workspace,
        'folder': folder,
        'document': document,
        'versions': versions,
        'user_member': member
    })

@login_required
def file_list(request):
    """List all files across all workspaces the user has access to."""
    documents = WorkspaceDocument.objects.filter(
        folder__workspace__members__user=request.user
    ).distinct()
    
    return render(request, 'workspace/documents/file_list.html', {
        'documents': documents,
        'title': 'Tous les fichiers'
    })

@login_required
def recent_files(request):
    """Show recently accessed files."""
    documents = WorkspaceDocument.objects.filter(
        folder__workspace__members__user=request.user
    ).order_by('-updated_at')[:20]
    
    return render(request, 'workspace/documents/recent_files.html', {
        'documents': documents,
        'title': 'Fichiers récents'
    })

@login_required
def shared_files(request):
    """Show files shared with the user."""
    documents = WorkspaceDocument.objects.filter(
        folder__workspace__members__user=request.user,
        shares__isnull=False
    ).distinct()
    
    return render(request, 'workspace/documents/shared_files.html', {
        'documents': documents,
        'title': 'Fichiers partagés'
    }) 