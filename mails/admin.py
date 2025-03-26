from django.contrib import admin
from .models import Email, EmailTemplate, EmailAttachment

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'category', 'is_system', 'created_at')
    list_filter = ('category', 'is_system')
    search_fields = ('name', 'subject', 'body_html', 'body_text')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    fieldsets = (
        (None, {
            'fields': ('name', 'subject', 'body_html', 'body_text', 'variables', 'category', 'is_system')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # Si c'est une création
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'recipient_email', 'status', 'priority', 'created_at')
    list_filter = ('status', 'priority', 'template', 'created_at')
    search_fields = ('subject', 'recipient_email', 'recipient_name', 'body_html', 'body_text')
    readonly_fields = ('created_at', 'updated_at', 'sent_at', 'created_by', 'updated_by')
    fieldsets = (
        (None, {
            'fields': ('recipient_email', 'recipient_name', 'cc', 'bcc', 'subject', 'body_html', 'body_text', 'priority', 'status', 'template')
        }),
        ('Entité liée', {
            'fields': ('related_entity_type', 'related_entity_id'),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at', 'sent_at', 'sender', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # Si c'est une création
            obj.created_by = request.user
            obj.sender = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(EmailAttachment)
class EmailAttachmentAdmin(admin.ModelAdmin):
    list_display = ('filename', 'email', 'mime_type', 'file_size', 'created_at')
    list_filter = ('mime_type', 'created_at')
    search_fields = ('filename', 'email__subject')
    readonly_fields = ('created_at', 'file_size')
    fieldsets = (
        (None, {
            'fields': ('email', 'file', 'filename', 'mime_type', 'file_size')
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
