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
from django.db import models

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

class TaskCalendarView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_calendar.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(
            created_by=self.request.user
        ).select_related('workflow_instance', 'assigned_to')

class MyTasksView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(
            created_by=self.request.user
        ).select_related('workflow_instance', 'assigned_to')

class AssignedTasksView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(
            assigned_to=self.request.user
        ).select_related('workflow_instance', 'assigned_to')

class UrgentTasksView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(
            priority='urgent'
        ).select_related('workflow_instance', 'assigned_to')

class HighPriorityTasksView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(
            priority='high'
        ).select_related('workflow_instance', 'assigned_to')

class MediumPriorityTasksView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(
            priority='medium'
        ).select_related('workflow_instance', 'assigned_to')

class LowPriorityTasksView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(
            priority='low'
        ).select_related('workflow_instance', 'assigned_to')

class PendingTasksView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(
            status='pending'
        ).select_related('workflow_instance', 'assigned_to')

class InProgressTasksView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(
            status='in_progress'
        ).select_related('workflow_instance', 'assigned_to')

class CompletedTasksView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(
            status='completed'
        ).select_related('workflow_instance', 'assigned_to')

class TaskReportView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_report.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = self.get_queryset()
        
        # Statistiques générales
        context['total_tasks'] = tasks.count()
        context['completed_tasks'] = tasks.filter(status='completed').count()
        context['pending_tasks'] = tasks.filter(status='pending').count()
        context['in_progress_tasks'] = tasks.filter(status='in_progress').count()
        
        # Statistiques par priorité
        context['urgent_tasks'] = tasks.filter(priority='urgent').count()
        context['high_priority_tasks'] = tasks.filter(priority='high').count()
        context['medium_priority_tasks'] = tasks.filter(priority='medium').count()
        context['low_priority_tasks'] = tasks.filter(priority='low').count()
        
        # Statistiques par utilisateur
        context['tasks_by_user'] = tasks.values('assigned_to__username').annotate(
            count=models.Count('id')
        ).order_by('-count')
        
        return context

class PerformanceReportView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/performance_report.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = self.get_queryset()
        
        # Statistiques de performance
        context['completion_rate'] = (tasks.filter(status='completed').count() / tasks.count() * 100) if tasks.exists() else 0
        context['on_time_tasks'] = tasks.filter(
            status='completed',
            completed_at__lte=models.F('due_date')
        ).count()
        context['late_tasks'] = tasks.filter(
            status='completed',
            completed_at__gt=models.F('due_date')
        ).count()
        
        # Temps moyen de complétion
        completed_tasks = tasks.filter(status='completed')
        if completed_tasks.exists():
            avg_completion_time = completed_tasks.annotate(
                completion_duration=models.ExpressionWrapper(
                    models.F('completed_at') - models.F('created_at'),
                    output_field=models.DurationField()
                )
            ).aggregate(avg_duration=models.Avg('completion_duration'))
            context['avg_completion_time'] = avg_completion_time['avg_duration']
        
        return context

class WorkloadReportView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/workload_report.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = self.get_queryset()
        
        # Charge de travail par utilisateur
        context['workload_by_user'] = tasks.values(
            'assigned_to__username'
        ).annotate(
            total_tasks=models.Count('id'),
            completed_tasks=models.Count('id', filter=models.Q(status='completed')),
            pending_tasks=models.Count('id', filter=models.Q(status='pending')),
            in_progress_tasks=models.Count('id', filter=models.Q(status='in_progress'))
        ).order_by('-total_tasks')
        
        # Charge de travail par statut
        context['workload_by_status'] = tasks.values('status').annotate(
            count=models.Count('id')
        ).order_by('status')
        
        # Charge de travail par priorité
        context['workload_by_priority'] = tasks.values('priority').annotate(
            count=models.Count('id')
        ).order_by('priority')
        
        return context

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