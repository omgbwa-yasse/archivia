from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    # LDAP Configuration
    path('ldap/', views.ldap_config_list, name='ldap_config_list'),
    path('ldap/create/', views.ldap_config_create, name='ldap_config_create'),
    path('ldap/<int:pk>/', views.ldap_config_detail, name='ldap_config_detail'),
    path('ldap/<int:pk>/edit/', views.ldap_config_edit, name='ldap_config_edit'),
    path('ldap/<int:pk>/delete/', views.ldap_config_delete, name='ldap_config_delete'),
    path('ldap/<int:pk>/test/', views.ldap_config_test, name='ldap_config_test'),
    
    # Backup Configuration
    path('backup/', views.backup_config_list, name='backup_config_list'),
    path('backup/create/', views.backup_config_create, name='backup_config_create'),
    path('backup/<int:pk>/', views.backup_config_detail, name='backup_config_detail'),
    path('backup/<int:pk>/edit/', views.backup_config_edit, name='backup_config_edit'),
    path('backup/<int:pk>/delete/', views.backup_config_delete, name='backup_config_delete'),
    path('backup/<int:pk>/start/', views.backup_config_start, name='backup_config_start'),
    path('backup/<int:pk>/logs/', views.backup_config_logs, name='backup_config_logs'),
] 