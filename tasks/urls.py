from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    # Workflow Definition URLs
    path('workflow-definitions/', views.WorkflowDefinitionListView.as_view(), name='workflow_definition_list'),
    path('workflow-definitions/create/', views.WorkflowDefinitionCreateView.as_view(), name='workflow_definition_create'),
    path('workflow-definitions/<int:pk>/', views.WorkflowDefinitionDetailView.as_view(), name='workflow_definition_detail'),
    path('workflow-definitions/<int:pk>/edit/', views.WorkflowDefinitionUpdateView.as_view(), name='workflow_definition_update'),
    path('workflow-definitions/<int:pk>/delete/', views.WorkflowDefinitionDeleteView.as_view(), name='workflow_definition_delete'),
    
    # Workflow Instance URLs
    path('workflow-instances/', views.WorkflowInstanceListView.as_view(), name='workflow_instance_list'),
    path('workflow-instances/create/', views.WorkflowInstanceCreateView.as_view(), name='workflow_instance_create'),
    path('workflow-instances/<int:pk>/', views.WorkflowInstanceDetailView.as_view(), name='workflow_instance_detail'),
    path('workflow-instances/<int:pk>/edit/', views.WorkflowInstanceUpdateView.as_view(), name='workflow_instance_update'),
    path('workflow-instances/<int:pk>/delete/', views.WorkflowInstanceDeleteView.as_view(), name='workflow_instance_delete'),
    
    # Task URLs
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('tasks/<int:pk>/complete/', views.TaskCompleteView.as_view(), name='task_complete'),
    path('tasks/calendar/', views.TaskCalendarView.as_view(), name='task_calendar'),
    path('tasks/my/', views.MyTasksView.as_view(), name='my_tasks'),
    path('tasks/assigned/', views.AssignedTasksView.as_view(), name='assigned_tasks'),
    path('tasks/urgent/', views.UrgentTasksView.as_view(), name='urgent_tasks'),
    path('tasks/high-priority/', views.HighPriorityTasksView.as_view(), name='high_priority'),
    path('tasks/medium-priority/', views.MediumPriorityTasksView.as_view(), name='medium_priority'),
    path('tasks/low-priority/', views.LowPriorityTasksView.as_view(), name='low_priority'),
    path('tasks/pending/', views.PendingTasksView.as_view(), name='pending_tasks'),
    path('tasks/in-progress/', views.InProgressTasksView.as_view(), name='in_progress'),
    path('tasks/completed/', views.CompletedTasksView.as_view(), name='completed_tasks'),
    path('tasks/report/', views.TaskReportView.as_view(), name='task_report'),
    path('tasks/performance/', views.PerformanceReportView.as_view(), name='performance_report'),
    path('tasks/workload/', views.WorkloadReportView.as_view(), name='workload_report'),
    
    # API endpoints for task status updates
    path('api/tasks/<int:pk>/status/', views.TaskStatusUpdateView.as_view(), name='task_status_update'),
    path('api/tasks/<int:pk>/assign/', views.TaskAssignView.as_view(), name='task_assign'),
] 