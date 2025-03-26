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
] 