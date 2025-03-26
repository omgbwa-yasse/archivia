from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.utils import timezone
from .models import Project, ProjectMember, ProjectTask, ProjectResource, TaskDependency, TaskComment, TimeEntry
from .forms import (
    ProjectForm, ProjectMemberForm, ProjectTaskForm, ProjectResourceForm,
    TaskDependencyForm, TaskCommentForm, TimeEntryForm
)

@login_required
def project_list(request):
    projects = Project.objects.filter(
        Q(owner=request.user) |
        Q(members__user=request.user)
    ).distinct()
    return render(request, 'projects/project_list.html', {'projects': projects})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not project.members.filter(user=request.user).exists() and project.owner != request.user:
        messages.error(request, "Vous n'avez pas accès à ce projet.")
        return redirect('project_list')
    
    tasks = project.tasks.all()
    members = project.members.all()
    resources = project.resources.all()
    
    context = {
        'project': project,
        'tasks': tasks,
        'members': members,
        'resources': resources,
    }
    return render(request, 'projects/project_detail.html', context)

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            
            # Ajouter le créateur comme membre avec le rôle MANAGER
            ProjectMember.objects.create(
                project=project,
                user=request.user,
                role='MANAGER',
                created_by=request.user
            )
            
            messages.success(request, 'Projet créé avec succès.')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(initial={'owner': request.user})
    
    return render(request, 'projects/project_form.html', {'form': form, 'title': 'Nouveau projet'})

@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not project.members.filter(user=request.user, role='MANAGER').exists() and project.owner != request.user:
        messages.error(request, "Vous n'avez pas les droits pour modifier ce projet.")
        return redirect('project_detail', pk=pk)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.updated_by = request.user
            project.save()
            messages.success(request, 'Projet mis à jour avec succès.')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'projects/project_form.html', {'form': form, 'title': 'Modifier le projet'})

@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not project.members.filter(user=request.user, role='MANAGER').exists() and project.owner != request.user:
        messages.error(request, "Vous n'avez pas les droits pour supprimer ce projet.")
        return redirect('project_detail', pk=pk)
    
    if request.method == 'POST':
        project.deleted_by = request.user
        project.deleted_at = timezone.now()
        project.save()
        messages.success(request, 'Projet supprimé avec succès.')
        return redirect('project_list')
    
    return render(request, 'projects/project_confirm_delete.html', {'project': project})

@login_required
def project_member_add(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if not project.members.filter(user=request.user, role='MANAGER').exists() and project.owner != request.user:
        messages.error(request, "Vous n'avez pas les droits pour ajouter des membres.")
        return redirect('project_detail', pk=project_pk)
    
    if request.method == 'POST':
        form = ProjectMemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.project = project
            member.created_by = request.user
            member.save()
            messages.success(request, 'Membre ajouté avec succès.')
            return redirect('project_detail', pk=project_pk)
    else:
        form = ProjectMemberForm()
    
    return render(request, 'projects/member_form.html', {'form': form, 'project': project})

@login_required
def project_member_remove(request, project_pk, member_pk):
    project = get_object_or_404(Project, pk=project_pk)
    member = get_object_or_404(ProjectMember, pk=member_pk, project=project)
    
    if not project.members.filter(user=request.user, role='MANAGER').exists() and project.owner != request.user:
        messages.error(request, "Vous n'avez pas les droits pour supprimer des membres.")
        return redirect('project_detail', pk=project_pk)
    
    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Membre supprimé avec succès.')
        return redirect('project_detail', pk=project_pk)
    
    return render(request, 'projects/member_confirm_delete.html', {'member': member})

@login_required
def task_list(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if not project.members.filter(user=request.user).exists() and project.owner != request.user:
        messages.error(request, "Vous n'avez pas accès aux tâches de ce projet.")
        return redirect('project_list')
    
    tasks = project.tasks.all()
    return render(request, 'projects/task_list.html', {'project': project, 'tasks': tasks})

@login_required
def task_detail(request, project_pk, task_pk):
    project = get_object_or_404(Project, pk=project_pk)
    task = get_object_or_404(ProjectTask, pk=task_pk, project=project)
    
    if not project.members.filter(user=request.user).exists() and project.owner != request.user:
        messages.error(request, "Vous n'avez pas accès à cette tâche.")
        return redirect('project_list')
    
    comments = task.comments.all()
    time_entries = task.time_entries.all()
    dependencies = task.dependencies.all()
    
    context = {
        'project': project,
        'task': task,
        'comments': comments,
        'time_entries': time_entries,
        'dependencies': dependencies,
    }
    return render(request, 'projects/task_detail.html', context)

@login_required
def task_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if not project.members.filter(user=request.user).exists() and project.owner != request.user:
        messages.error(request, "Vous n'avez pas les droits pour créer des tâches.")
        return redirect('project_detail', pk=project_pk)
    
    if request.method == 'POST':
        form = ProjectTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.created_by = request.user
            task.save()
            messages.success(request, 'Tâche créée avec succès.')
            return redirect('task_detail', project_pk=project_pk, task_pk=task.pk)
    else:
        form = ProjectTaskForm(initial={'project': project})
    
    return render(request, 'projects/task_form.html', {'form': form, 'project': project, 'title': 'Nouvelle tâche'})

@login_required
def task_edit(request, project_pk, task_pk):
    project = get_object_or_404(Project, pk=project_pk)
    task = get_object_or_404(ProjectTask, pk=task_pk, project=project)
    
    if not project.members.filter(user=request.user).exists() and project.owner != request.user:
        messages.error(request, "Vous n'avez pas les droits pour modifier cette tâche.")
        return redirect('task_detail', project_pk=project_pk, task_pk=task_pk)
    
    if request.method == 'POST':
        form = ProjectTaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.updated_by = request.user
            task.save()
            messages.success(request, 'Tâche mise à jour avec succès.')
            return redirect('task_detail', project_pk=project_pk, task_pk=task.pk)
    else:
        form = ProjectTaskForm(instance=task)
    
    return render(request, 'projects/task_form.html', {'form': form, 'project': project, 'title': 'Modifier la tâche'})

@login_required
def task_delete(request, project_pk, task_pk):
    project = get_object_or_404(Project, pk=project_pk)
    task = get_object_or_404(ProjectTask, pk=task_pk, project=project)
    
    if not project.members.filter(user=request.user).exists() and project.owner != request.user:
        messages.error(request, "Vous n'avez pas les droits pour supprimer cette tâche.")
        return redirect('task_detail', project_pk=project_pk, task_pk=task_pk)
    
    if request.method == 'POST':
        task.deleted_by = request.user
        task.deleted_at = timezone.now()
        task.save()
        messages.success(request, 'Tâche supprimée avec succès.')
        return redirect('task_list', project_pk=project_pk)
    
    return render(request, 'projects/task_confirm_delete.html', {'project': project, 'task': task})

@login_required
def task_comment_add(request, project_pk, task_pk):
    project = get_object_or_404(Project, pk=project_pk)
    task = get_object_or_404(ProjectTask, pk=task_pk, project=project)
    
    if not project.members.filter(user=request.user).exists() and project.owner != request.user:
        messages.error(request, "Vous n'avez pas les droits pour ajouter des commentaires.")
        return redirect('task_detail', project_pk=project_pk, task_pk=task_pk)
    
    if request.method == 'POST':
        form = TaskCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.created_by = request.user
            comment.save()
            messages.success(request, 'Commentaire ajouté avec succès.')
            return redirect('task_detail', project_pk=project_pk, task_pk=task_pk)
    else:
        form = TaskCommentForm(initial={'task': task})
    
    return render(request, 'projects/comment_form.html', {'form': form, 'project': project, 'task': task})

@login_required
def task_time_entry_add(request, project_pk, task_pk):
    project = get_object_or_404(Project, pk=project_pk)
    task = get_object_or_404(ProjectTask, pk=task_pk, project=project)
    
    if not project.members.filter(user=request.user).exists() and project.owner != request.user:
        messages.error(request, "Vous n'avez pas les droits pour ajouter des entrées de temps.")
        return redirect('task_detail', project_pk=project_pk, task_pk=task_pk)
    
    if request.method == 'POST':
        form = TimeEntryForm(request.POST)
        if form.is_valid():
            time_entry = form.save(commit=False)
            time_entry.task = task
            time_entry.user = request.user
            time_entry.created_by = request.user
            time_entry.save()
            messages.success(request, 'Entrée de temps ajoutée avec succès.')
            return redirect('task_detail', project_pk=project_pk, task_pk=task_pk)
    else:
        form = TimeEntryForm(initial={'task': task, 'user': request.user})
    
    return render(request, 'projects/time_entry_form.html', {'form': form, 'project': project, 'task': task})

@login_required
def task_dependency_add(request, project_pk, task_pk):
    project = get_object_or_404(Project, pk=project_pk)
    task = get_object_or_404(ProjectTask, pk=task_pk, project=project)
    
    if not project.members.filter(user=request.user).exists() and project.owner != request.user:
        messages.error(request, "Vous n'avez pas les droits pour ajouter des dépendances.")
        return redirect('task_detail', project_pk=project_pk, task_pk=task_pk)
    
    if request.method == 'POST':
        form = TaskDependencyForm(request.POST)
        if form.is_valid():
            dependency = form.save(commit=False)
            dependency.task = task
            dependency.created_by = request.user
            dependency.save()
            messages.success(request, 'Dépendance ajoutée avec succès.')
            return redirect('task_detail', project_pk=project_pk, task_pk=task_pk)
    else:
        form = TaskDependencyForm(initial={'task': task})
    
    return render(request, 'projects/dependency_form.html', {'form': form, 'project': project, 'task': task})

@login_required
def resource_list(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if not project.members.filter(user=request.user).exists() and project.owner != request.user:
        messages.error(request, "Vous n'avez pas accès aux ressources de ce projet.")
        return redirect('project_list')
    
    resources = project.resources.all()
    return render(request, 'projects/resource_list.html', {'project': project, 'resources': resources})

@login_required
def resource_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if not project.members.filter(user=request.user).exists() and project.owner != request.user:
        messages.error(request, "Vous n'avez pas les droits pour créer des ressources.")
        return redirect('project_detail', pk=project_pk)
    
    if request.method == 'POST':
        form = ProjectResourceForm(request.POST)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.project = project
            resource.created_by = request.user
            resource.save()
            messages.success(request, 'Ressource créée avec succès.')
            return redirect('resource_list', project_pk=project_pk)
    else:
        form = ProjectResourceForm(initial={'project': project})
    
    return render(request, 'projects/resource_form.html', {'form': form, 'project': project, 'title': 'Nouvelle ressource'})

@login_required
def resource_edit(request, project_pk, resource_pk):
    project = get_object_or_404(Project, pk=project_pk)
    resource = get_object_or_404(ProjectResource, pk=resource_pk, project=project)
    
    if not project.members.filter(user=request.user).exists() and project.owner != request.user:
        messages.error(request, "Vous n'avez pas les droits pour modifier cette ressource.")
        return redirect('resource_list', project_pk=project_pk)
    
    if request.method == 'POST':
        form = ProjectResourceForm(request.POST, instance=resource)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.updated_by = request.user
            resource.save()
            messages.success(request, 'Ressource mise à jour avec succès.')
            return redirect('resource_list', project_pk=project_pk)
    else:
        form = ProjectResourceForm(instance=resource)
    
    return render(request, 'projects/resource_form.html', {'form': form, 'project': project, 'title': 'Modifier la ressource'})

@login_required
def resource_delete(request, project_pk, resource_pk):
    project = get_object_or_404(Project, pk=project_pk)
    resource = get_object_or_404(ProjectResource, pk=resource_pk, project=project)
    
    if not project.members.filter(user=request.user).exists() and project.owner != request.user:
        messages.error(request, "Vous n'avez pas les droits pour supprimer cette ressource.")
        return redirect('resource_list', project_pk=project_pk)
    
    if request.method == 'POST':
        resource.deleted_by = request.user
        resource.deleted_at = timezone.now()
        resource.save()
        messages.success(request, 'Ressource supprimée avec succès.')
        return redirect('resource_list', project_pk=project_pk)
    
    return render(request, 'projects/resource_confirm_delete.html', {'project': project, 'resource': resource})

@login_required
@require_POST
def task_status_update(request, project_pk, task_pk):
    project = get_object_or_404(Project, pk=project_pk)
    task = get_object_or_404(ProjectTask, pk=task_pk, project=project)
    
    if not project.members.filter(user=request.user).exists() and project.owner != request.user:
        return JsonResponse({'error': "Vous n'avez pas les droits pour modifier le statut de cette tâche."}, status=403)
    
    new_status = request.POST.get('status')
    if new_status in dict(ProjectTask.STATUS_CHOICES):
        task.status = new_status
        if new_status == 'DONE':
            task.completed_at = timezone.now()
        task.updated_by = request.user
        task.save()
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'error': 'Statut invalide.'}, status=400) 