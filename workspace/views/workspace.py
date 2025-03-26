from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from ..models import Workspace, WorkspaceMember
from ..forms import WorkspaceForm
from django.utils import timezone

@login_required
def workspace_list(request):
    """List all workspaces the user has access to."""
    workspaces = Workspace.objects.filter(
        members__user=request.user
    ).distinct()
    
    paginator = Paginator(workspaces, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'workspace/workspace_list.html', {
        'page_obj': page_obj
    })

@login_required
def workspace_detail(request, pk):
    """Show details of a specific workspace."""
    workspace = get_object_or_404(Workspace, pk=pk)
    member = get_object_or_404(WorkspaceMember, workspace=workspace, user=request.user)
    
    return render(request, 'workspace/workspace_detail.html', {
        'workspace': workspace,
        'member': member
    })

@login_required
def workspace_create(request):
    """Create a new workspace."""
    if request.method == 'POST':
        form = WorkspaceForm(request.POST)
        if form.is_valid():
            workspace = form.save(commit=False)
            workspace.owner = request.user
            workspace.created_by = request.user
            workspace.save()
            
            # Add the creator as an admin member
            WorkspaceMember.objects.create(
                workspace=workspace,
                user=request.user,
                role='admin',
                created_by=request.user
            )
            
            messages.success(request, 'Workspace created successfully.')
            return redirect('workspace:workspace_detail', pk=workspace.pk)
    else:
        form = WorkspaceForm()
    
    return render(request, 'workspace/workspace_form.html', {
        'form': form,
        'title': 'Create Workspace'
    })

@login_required
def workspace_edit(request, pk):
    """Edit an existing workspace."""
    workspace = get_object_or_404(Workspace, pk=pk)
    member = get_object_or_404(WorkspaceMember, workspace=workspace, user=request.user)
    
    if member.role != 'admin':
        messages.error(request, 'You do not have permission to edit this workspace.')
        return redirect('workspace:workspace_detail', pk=pk)
    
    if request.method == 'POST':
        form = WorkspaceForm(request.POST, instance=workspace)
        if form.is_valid():
            workspace = form.save(commit=False)
            workspace.updated_by = request.user
            workspace.save()
            messages.success(request, 'Workspace updated successfully.')
            return redirect('workspace:workspace_detail', pk=pk)
    else:
        form = WorkspaceForm(instance=workspace)
    
    return render(request, 'workspace/workspace_form.html', {
        'form': form,
        'title': 'Edit Workspace',
        'workspace': workspace
    })

@login_required
@require_http_methods(["POST"])
def workspace_delete(request, pk):
    """Delete a workspace."""
    workspace = get_object_or_404(Workspace, pk=pk)
    member = get_object_or_404(WorkspaceMember, workspace=workspace, user=request.user)
    
    if member.role != 'admin':
        return JsonResponse({
            'status': 'error',
            'message': 'You do not have permission to delete this workspace.'
        }, status=403)
    
    workspace.deleted_by = request.user
    workspace.deleted_at = timezone.now()
    workspace.save()
    
    return JsonResponse({
        'status': 'success',
        'message': 'Workspace deleted successfully.'
    }) 