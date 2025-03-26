from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views import View
from .models import Task, WorkflowInstance, WorkflowDefinition
from .forms import TaskForm, WorkflowDefinitionForm, WorkflowInstanceForm

# Workflow Definition Views
class WorkflowDefinitionListView(LoginRequiredMixin, ListView):
    model = WorkflowDefinition
    template_name = 'tasks/workflow_definition_list.html'
    context_object_name = 'workflow_definitions'

class WorkflowDefinitionCreateView(LoginRequiredMixin, CreateView):
    model = WorkflowDefinition
    form_class = WorkflowDefinitionForm
    template_name = 'tasks/workflow_definition_form.html'
    success_url = reverse_lazy('tasks:workflow_definition_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class WorkflowDefinitionDetailView(LoginRequiredMixin, DetailView):
    model = WorkflowDefinition
    template_name = 'tasks/workflow_definition_detail.html'
    context_object_name = 'workflow_definition'

class WorkflowDefinitionUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkflowDefinition
    form_class = WorkflowDefinitionForm
    template_name = 'tasks/workflow_definition_form.html'
    success_url = reverse_lazy('tasks:workflow_definition_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class WorkflowDefinitionDeleteView(LoginRequiredMixin, DeleteView):
    model = WorkflowDefinition
    template_name = 'tasks/workflow_definition_confirm_delete.html'
    success_url = reverse_lazy('tasks:workflow_definition_list')

# Workflow Instance Views
class WorkflowInstanceListView(LoginRequiredMixin, ListView):
    model = WorkflowInstance
    template_name = 'tasks/workflow_instance_list.html'
    context_object_name = 'workflow_instances'

class WorkflowInstanceCreateView(LoginRequiredMixin, CreateView):
    model = WorkflowInstance
    form_class = WorkflowInstanceForm
    template_name = 'tasks/workflow_instance_form.html'
    success_url = reverse_lazy('tasks:workflow_instance_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class WorkflowInstanceDetailView(LoginRequiredMixin, DetailView):
    model = WorkflowInstance
    template_name = 'tasks/workflow_instance_detail.html'
    context_object_name = 'workflow_instance'

class WorkflowInstanceUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkflowInstance
    form_class = WorkflowInstanceForm
    template_name = 'tasks/workflow_instance_form.html'
    success_url = reverse_lazy('tasks:workflow_instance_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class WorkflowInstanceDeleteView(LoginRequiredMixin, DeleteView):
    model = WorkflowInstance
    template_name = 'tasks/workflow_instance_confirm_delete.html'
    success_url = reverse_lazy('tasks:workflow_instance_list')

# Task Views
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:task_list')

class TaskCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.complete(request.user)
        messages.success(request, 'Tâche marquée comme terminée.')
        return redirect('tasks:task_list')

class TaskStatusUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        status = request.POST.get('status')
        if status in dict(Task.STATUS_CHOICES):
            task.status = status
            task.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Invalid status'})

class TaskAssignView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        user_id = request.POST.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            task.assigned_to = user
            task.save()
            return JsonResponse({'status': 'success'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'})

# Legacy function-based views - can be removed once templates are updated
@login_required
def task_list(request):
    return TaskListView.as_view()(request)

@login_required
def task_create(request):
    return TaskCreateView.as_view()(request)

@login_required
def task_edit(request, pk):
    return TaskUpdateView.as_view()(request, pk=pk)

@login_required
def task_delete(request, pk):
    return TaskDeleteView.as_view()(request, pk=pk)

@login_required
def task_complete(request, pk):
    return TaskCompleteView.as_view()(request, pk=pk) 