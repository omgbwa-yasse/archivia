from django.contrib import admin
from .models import Email, EmailTemplate, EmailAttachment, Folder, Contact, ContactGroup

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['subject', 'sender', 'is_sent', 'sent_at']
    list_filter = ['is_sent', 'is_important', 'is_flagged']
    search_fields = ['subject', 'body_html', 'body_text']
    readonly_fields = ['created_at', 'updated_at', 'sent_at']

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'category', 'is_system']
    list_filter = ['category', 'is_system']
    search_fields = ['name', 'subject', 'body_html', 'body_text']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

@admin.register(EmailAttachment)
class EmailAttachmentAdmin(admin.ModelAdmin):
    list_display = ['filename', 'email', 'created_at']
    search_fields = ['filename']
    readonly_fields = ['created_at']

@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'created_at']
    list_filter = ['parent']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'company']
    list_filter = ['groups']
    search_fields = ['first_name', 'last_name', 'email', 'company']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ContactGroup)
class ContactGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
