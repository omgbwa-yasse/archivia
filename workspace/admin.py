from django.contrib import admin
from .models import (
    Workspace,
    WorkspaceMember,
    WorkspaceFolder,
    WorkspaceDocument,
    WorkspaceDocumentVersion,
    WorkspaceDocumentPermission,
    WorkspaceDocumentShare
)

@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'deleted_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')

@admin.register(WorkspaceMember)
class WorkspaceMemberAdmin(admin.ModelAdmin):
    list_display = ('workspace', 'user', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('workspace__name', 'user__username')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(WorkspaceFolder)
class WorkspaceFolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'workspace', 'parent_folder', 'created_at')
    list_filter = ('workspace', 'created_at', 'deleted_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')

@admin.register(WorkspaceDocument)
class WorkspaceDocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'folder', 'file_type', 'version', 'is_locked', 'created_at')
    list_filter = ('file_type', 'is_locked', 'created_at', 'deleted_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')

@admin.register(WorkspaceDocumentVersion)
class WorkspaceDocumentVersionAdmin(admin.ModelAdmin):
    list_display = ('document', 'version', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('document__name', 'change_summary')
    readonly_fields = ('created_at',)

@admin.register(WorkspaceDocumentPermission)
class WorkspaceDocumentPermissionAdmin(admin.ModelAdmin):
    list_display = ('document', 'user', 'group', 'permission_type', 'created_at')
    list_filter = ('permission_type', 'created_at')
    search_fields = ('document__name', 'user__username', 'group__name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(WorkspaceDocumentShare)
class WorkspaceDocumentShareAdmin(admin.ModelAdmin):
    list_display = ('document', 'share_token', 'expires_at', 'access_count', 'created_at')
    list_filter = ('password_protected', 'created_at', 'expires_at')
    search_fields = ('document__name', 'share_token')
    readonly_fields = ('created_at', 'access_count') 