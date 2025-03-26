from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Task, WorkflowInstance
from .forms import TaskForm

@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            messages.success(request, 'Tâche créée avec succès.')
            return redirect('task_list')
    else:
        form = TaskForm()
    
    context = {
        'form': form,
        'users': User.objects.all(),
        'workflow_instances': WorkflowInstance.objects.all()
    }
    return render(request, 'tasks/task_form.html', context)

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.updated_by = request.user
            task.save()
            messages.success(request, 'Tâche mise à jour avec succès.')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    
    context = {
        'form': form,
        'task': task,
        'users': User.objects.all(),
        'workflow_instances': WorkflowInstance.objects.all()
    }
    return render(request, 'tasks/task_form.html', context)

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Tâche supprimée avec succès.')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.complete(request.user)
    messages.success(request, 'Tâche marquée comme terminée.')
    return redirect('task_list') 