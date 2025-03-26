from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from ..models import Workspace, WorkspaceMember
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def workspace_member_list(request, workspace_pk):
    """List all members of a workspace."""
    workspace = get_object_or_404(Workspace, pk=workspace_pk)
    member = get_object_or_404(WorkspaceMember, workspace=workspace, user=request.user)
    
    members = WorkspaceMember.objects.filter(workspace=workspace)
    
    return render(request, 'workspace/member_list.html', {
        'workspace': workspace,
        'members': members,
        'user_member': member
    })

@login_required
def workspace_member_add(request, workspace_pk):
    """Add a new member to the workspace."""
    workspace = get_object_or_404(Workspace, pk=workspace_pk)
    member = get_object_or_404(WorkspaceMember, workspace=workspace, user=request.user)
    
    if member.role != 'admin':
        messages.error(request, 'You do not have permission to add members to this workspace.')
        return redirect('workspace:workspace_member_list', workspace_pk=workspace_pk)
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        role = request.POST.get('role', 'member')
        
        try:
            user = User.objects.get(id=user_id)
            WorkspaceMember.objects.create(
                workspace=workspace,
                user=user,
                role=role,
                created_by=request.user
            )
            messages.success(request, f'{user.get_full_name()} has been added to the workspace.')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
        except Exception as e:
            messages.error(request, str(e))
        
        return redirect('workspace:workspace_member_list', workspace_pk=workspace_pk)
    
    return render(request, 'workspace/member_form.html', {
        'workspace': workspace,
        'users': User.objects.all()
    })

@login_required
def workspace_member_edit(request, workspace_pk, pk):
    """Edit a workspace member's role."""
    workspace = get_object_or_404(Workspace, pk=workspace_pk)
    admin_member = get_object_or_404(WorkspaceMember, workspace=workspace, user=request.user)
    member = get_object_or_404(WorkspaceMember, pk=pk, workspace=workspace)
    
    if admin_member.role != 'admin':
        messages.error(request, 'You do not have permission to edit member roles.')
        return redirect('workspace:workspace_member_list', workspace_pk=workspace_pk)
    
    if request.method == 'POST':
        role = request.POST.get('role')
        if role in ['admin', 'member']:
            member.role = role
            member.updated_by = request.user
            member.save()
            messages.success(request, f"{member.user.get_full_name()}'s role has been updated.")
        else:
            messages.error(request, 'Invalid role.')
        
        return redirect('workspace:workspace_member_list', workspace_pk=workspace_pk)
    
    return render(request, 'workspace/member_form.html', {
        'workspace': workspace,
        'member': member
    })

@login_required
@require_http_methods(["POST"])
def workspace_member_remove(request, workspace_pk, pk):
    """Remove a member from the workspace."""
    workspace = get_object_or_404(Workspace, pk=workspace_pk)
    admin_member = get_object_or_404(WorkspaceMember, workspace=workspace, user=request.user)
    member = get_object_or_404(WorkspaceMember, pk=pk, workspace=workspace)
    
    if admin_member.role != 'admin':
        return JsonResponse({
            'status': 'error',
            'message': 'You do not have permission to remove members from this workspace.'
        }, status=403)
    
    if member.role == 'admin' and workspace.members.filter(role='admin').count() == 1:
        return JsonResponse({
            'status': 'error',
            'message': 'Cannot remove the last admin from the workspace.'
        }, status=400)
    
    member.delete()
    
    return JsonResponse({
        'status': 'success',
        'message': f'{member.user.get_full_name()} has been removed from the workspace.'
    })

@login_required
def member_list(request):
    """List all members across all workspaces."""
    members = WorkspaceMember.objects.filter(
        workspace__members__user=request.user
    ).distinct()
    
    return render(request, 'workspace/members/member_list.html', {
        'members': members,
        'title': 'Tous les membres'
    })

@login_required
def roles(request):
    """View and manage workspace roles and permissions."""
    return render(request, 'workspace/members/roles.html', {
        'title': 'Rôles et permissions'
    }) 