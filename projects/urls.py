from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    # Projets
    path('', views.project_list, name='project_list'),
    path('create/', views.project_create, name='project_create'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('<int:pk>/delete/', views.project_delete, name='project_delete'),
    
    # Membres du projet
    path('<int:project_pk>/members/add/', views.project_member_add, name='project_member_add'),
    path('<int:project_pk>/members/<int:member_pk>/remove/', views.project_member_remove, name='project_member_remove'),
    
    # Tâches
    path('<int:project_pk>/tasks/', views.task_list, name='task_list'),
    path('<int:project_pk>/tasks/create/', views.task_create, name='task_create'),
    path('<int:project_pk>/tasks/<int:task_pk>/', views.task_detail, name='task_detail'),
    path('<int:project_pk>/tasks/<int:task_pk>/edit/', views.task_edit, name='task_edit'),
    path('<int:project_pk>/tasks/<int:task_pk>/delete/', views.task_delete, name='task_delete'),
    path('<int:project_pk>/tasks/<int:task_pk>/status/', views.task_status_update, name='task_status_update'),
    
    # Commentaires sur les tâches
    path('<int:project_pk>/tasks/<int:task_pk>/comments/add/', views.task_comment_add, name='task_comment_add'),
    
    # Entrées de temps
    path('<int:project_pk>/tasks/<int:task_pk>/time/add/', views.task_time_entry_add, name='task_time_entry_add'),
    
    # Dépendances de tâches
    path('<int:project_pk>/tasks/<int:task_pk>/dependencies/add/', views.task_dependency_add, name='task_dependency_add'),
    
    # Ressources
    path('<int:project_pk>/resources/', views.resource_list, name='resource_list'),
    path('<int:project_pk>/resources/create/', views.resource_create, name='resource_create'),
    path('<int:project_pk>/resources/<int:resource_pk>/edit/', views.resource_edit, name='resource_edit'),
    path('<int:project_pk>/resources/<int:resource_pk>/delete/', views.resource_delete, name='resource_delete'),
] 