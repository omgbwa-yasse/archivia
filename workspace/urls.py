from django.urls import path
from . import views
from .views import members, folders, documents

app_name = 'workspace'

urlpatterns = [
    # Workspace URLs
    path('', views.workspace_list, name='workspace_list'),
    path('create/', views.workspace_create, name='workspace_create'),
    path('<int:pk>/', views.workspace_detail, name='workspace_detail'),
    path('<int:pk>/edit/', views.workspace_edit, name='workspace_edit'),
    path('<int:pk>/delete/', views.workspace_delete, name='workspace_delete'),
    
    # Workspace Member URLs
    path('<int:workspace_pk>/members/', members.workspace_member_list, name='workspace_member_list'),
    path('<int:workspace_pk>/members/add/', members.workspace_member_add, name='workspace_member_add'),
    path('<int:workspace_pk>/members/<int:pk>/edit/', members.workspace_member_edit, name='workspace_member_edit'),
    path('<int:workspace_pk>/members/<int:pk>/remove/', members.workspace_member_remove, name='workspace_member_remove'),
    
    # Global Member URLs
    path('members/', members.member_list, name='member_list'),
    path('roles/', members.roles, name='roles'),
    
    # Workspace Folder URLs
    path('<int:workspace_pk>/folders/', folders.folder_list, name='folder_list'),
    path('<int:workspace_pk>/folders/create/', folders.folder_create, name='folder_create'),
    path('<int:workspace_pk>/folders/<int:pk>/', folders.folder_detail, name='folder_detail'),
    path('<int:workspace_pk>/folders/<int:pk>/edit/', folders.folder_edit, name='folder_edit'),
    path('<int:workspace_pk>/folders/<int:pk>/delete/', folders.folder_delete, name='folder_delete'),
    
    # Workspace Document URLs
    path('<int:workspace_pk>/folders/<int:folder_pk>/documents/', documents.document_list, name='document_list'),
    path('<int:workspace_pk>/folders/<int:folder_pk>/documents/upload/', documents.document_upload, name='document_upload'),
    path('<int:workspace_pk>/folders/<int:folder_pk>/documents/<int:pk>/', documents.document_detail, name='document_detail'),
    path('<int:workspace_pk>/folders/<int:folder_pk>/documents/<int:pk>/edit/', documents.document_edit, name='document_edit'),
    path('<int:workspace_pk>/folders/<int:folder_pk>/documents/<int:pk>/delete/', documents.document_delete, name='document_delete'),
    path('<int:workspace_pk>/folders/<int:folder_pk>/documents/<int:pk>/download/', documents.document_download, name='document_download'),
    path('<int:workspace_pk>/folders/<int:folder_pk>/documents/<int:pk>/share/', documents.document_share, name='document_share'),
    path('<int:workspace_pk>/folders/<int:folder_pk>/documents/<int:pk>/versions/', documents.document_versions, name='document_versions'),
    
    # Global File URLs
    path('files/', documents.file_list, name='files'),
    path('files/recent/', documents.recent_files, name='files_recent'),
    path('files/shared/', documents.shared_files, name='files_shared'),
    
    # Activity URLs
    path('activity/', views.activity_log, name='activity_log'),
    path('notifications/', views.notifications, name='notifications'),
] 