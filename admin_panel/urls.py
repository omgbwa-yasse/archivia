from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    # LDAP Configuration
    path('ldap/', views.ldap_config_list, name='ldap_config_list'),
    path('ldap/create/', views.ldap_config_create, name='ldap_config_create'),
    path('ldap/<int:pk>/', views.ldap_config_detail, name='ldap_config_detail'),
    path('ldap/<int:pk>/edit/', views.ldap_config_edit, name='ldap_config_edit'),
    path('ldap/<int:pk>/sync/', views.ldap_sync, name='ldap_sync'),
    
    # Backup Configuration
    path('backup/', views.backup_config_list, name='backup_config_list'),
    path('backup/create/', views.backup_config_create, name='backup_config_create'),
    path('backup/<int:pk>/', views.backup_config_detail, name='backup_config_detail'),
    path('backup/<int:pk>/edit/', views.backup_config_edit, name='backup_config_edit'),
    path('backup/<int:pk>/start/', views.backup_start, name='backup_config_start'),
    path('backup/status/<int:backup_log_id>/', views.backup_status, name='backup_status'),
    path('backup/restore/<int:backup_log_id>/', views.restore_backup, name='restore_backup'),
    path('backup/restore/status/<int:restore_log_id>/', views.restore_status, name='restore_status'),
] 