from django.urls import path
from . import views

app_name = 'mails'

urlpatterns = [
    # Email Templates URLs
    path('templates/', views.template_list, name='template_list'),
    path('templates/create/', views.create_template, name='template_create'),
    path('templates/<int:pk>/edit/', views.edit_template, name='template_edit'),
    path('templates/<int:pk>/delete/', views.template_delete, name='template_delete'),
    
    # Emails URLs
    path('emails/', views.email_list, name='email_list'),
    path('emails/create/', views.create_email, name='email_create'),
    path('emails/<int:pk>/', views.email_detail, name='email_detail'),
    path('emails/<int:pk>/edit/', views.edit_email, name='email_edit'),
    path('emails/<int:pk>/delete/', views.email_delete, name='email_delete'),
    path('emails/<int:pk>/send/', views.email_send, name='email_send'),
    
    # Attachments URLs
    path('emails/<int:email_id>/attachments/<int:attachment_id>/download/', 
         views.download_attachment, name='download_attachment'),
         
    # Mailbox URLs
    path('compose/', views.create_email, name='compose'),
    path('inbox/', views.email_list, name='inbox'),
    path('sent/', views.email_list, name='sent'),
    path('drafts/', views.email_list, name='drafts'),
    path('trash/', views.email_list, name='trash'),
    
    # Folder URLs
    path('folders/', views.folder_list, name='folder_list'),
    path('folders/create/', views.folder_create, name='folder_create'),
    path('folders/<int:pk>/', views.folder_detail, name='folder_detail'),
    path('folders/<int:pk>/edit/', views.folder_edit, name='folder_edit'),
    path('folders/<int:pk>/delete/', views.folder_delete, name='folder_delete'),
    
    # Special folders
    path('important/', views.email_list, name='important'),
    path('flagged/', views.email_list, name='flagged'),
    
    # Contact URLs
    path('contacts/', views.contact_list, name='contact_list'),
    path('contacts/create/', views.contact_create, name='contact_create'),
    path('contacts/<int:pk>/', views.contact_detail, name='contact_detail'),
    path('contacts/<int:pk>/edit/', views.contact_edit, name='contact_edit'),
    path('contacts/<int:pk>/delete/', views.contact_delete, name='contact_delete'),
    path('contacts/import/', views.contact_import, name='contact_import'),
    
    # Contact Groups URLs
    path('groups/', views.group_list, name='groups'),
    path('groups/create/', views.group_create, name='group_create'),
    path('groups/<int:pk>/', views.group_detail, name='group_detail'),
    path('groups/<int:pk>/edit/', views.group_edit, name='group_edit'),
    path('groups/<int:pk>/delete/', views.group_delete, name='group_delete'),
    
    # Favorites
    path('favorites/', views.email_list, name='favorites'),
    
    # Tools URLs
    path('search/', views.email_search, name='search'),
    path('settings/', views.email_settings, name='settings'),
    path('archive/', views.email_archive, name='archive'),
] 