from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from ..models import Workspace, WorkspaceMember, WorkspaceFolder

@login_required
def folder_list(request, workspace_pk):
    """List all folders in a workspace."""
    workspace = get_object_or_404(Workspace, pk=workspace_pk)
    member = get_object_or_404(WorkspaceMember, workspace=workspace, user=request.user)
    
    folders = WorkspaceFolder.objects.filter(workspace=workspace)
    
    return render(request, 'workspace/folder_list.html', {
        'workspace': workspace,
        'folders': folders,
        'user_member': member
    })

@login_required
def folder_create(request, workspace_pk):
    """Create a new folder in the workspace."""
    workspace = get_object_or_404(Workspace, pk=workspace_pk)
    member = get_object_or_404(WorkspaceMember, workspace=workspace, user=request.user)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        parent_id = request.POST.get('parent_id')
        
        try:
            parent = None
            if parent_id:
                parent = get_object_or_404(WorkspaceFolder, pk=parent_id, workspace=workspace)
            
            folder = WorkspaceFolder.objects.create(
                workspace=workspace,
                name=name,
                description=description,
                parent=parent,
                created_by=request.user
            )
            messages.success(request, f'Folder "{name}" has been created.')
            return redirect('workspace:folder_detail', workspace_pk=workspace_pk, pk=folder.pk)
        except Exception as e:
            messages.error(request, str(e))
    
    return render(request, 'workspace/folder_form.html', {
        'workspace': workspace,
        'folders': WorkspaceFolder.objects.filter(workspace=workspace, parent=None),
        'user_member': member
    })

@login_required
def folder_detail(request, workspace_pk, pk):
    """View folder details and contents."""
    workspace = get_object_or_404(Workspace, pk=workspace_pk)
    member = get_object_or_404(WorkspaceMember, workspace=workspace, user=request.user)
    folder = get_object_or_404(WorkspaceFolder, pk=pk, workspace=workspace)
    
    subfolders = WorkspaceFolder.objects.filter(parent=folder)
    documents = folder.documents.all()
    
    return render(request, 'workspace/folder_detail.html', {
        'workspace': workspace,
        'folder': folder,
        'subfolders': subfolders,
        'documents': documents,
        'user_member': member
    })

@login_required
def folder_edit(request, workspace_pk, pk):
    """Edit a folder's details."""
    workspace = get_object_or_404(Workspace, pk=workspace_pk)
    member = get_object_or_404(WorkspaceMember, workspace=workspace, user=request.user)
    folder = get_object_or_404(WorkspaceFolder, pk=pk, workspace=workspace)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        parent_id = request.POST.get('parent_id')
        
        try:
            parent = None
            if parent_id and int(parent_id) != folder.pk:  # Prevent self-reference
                parent = get_object_or_404(WorkspaceFolder, pk=parent_id, workspace=workspace)
                if parent.is_descendant_of(folder):  # Prevent circular reference
                    raise ValueError("Cannot move a folder into its own subfolder.")
            
            folder.name = name
            folder.description = description
            folder.parent = parent
            folder.updated_by = request.user
            folder.save()
            
            messages.success(request, f'Folder "{name}" has been updated.')
            return redirect('workspace:folder_detail', workspace_pk=workspace_pk, pk=folder.pk)
        except Exception as e:
            messages.error(request, str(e))
    
    return render(request, 'workspace/folder_form.html', {
        'workspace': workspace,
        'folder': folder,
        'folders': WorkspaceFolder.objects.filter(workspace=workspace).exclude(pk=folder.pk),
        'user_member': member
    })

@login_required
@require_http_methods(["POST"])
def folder_delete(request, workspace_pk, pk):
    """Delete a folder and all its contents."""
    workspace = get_object_or_404(Workspace, pk=workspace_pk)
    member = get_object_or_404(WorkspaceMember, workspace=workspace, user=request.user)
    folder = get_object_or_404(WorkspaceFolder, pk=pk, workspace=workspace)
    
    try:
        name = folder.name
        folder.delete()
        messages.success(request, f'Folder "{name}" and all its contents have been deleted.')
    except Exception as e:
        messages.error(request, str(e))
    
    return redirect('workspace:folder_list', workspace_pk=workspace_pk) 