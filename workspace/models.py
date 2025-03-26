from django.db import models
from django.conf import settings
from django.utils import timezone

class Workspace(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='owned_workspaces')
    root_folder = models.ForeignKey('WorkspaceFolder', on_delete=models.SET_NULL, null=True, blank=True, related_name='root_workspace')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_workspaces')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_workspaces')
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='deleted_workspaces')
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['owner']),
            models.Index(fields=['created_by']),
            models.Index(fields=['updated_by']),
            models.Index(fields=['deleted_by']),
        ]

    def __str__(self):
        return self.name

class WorkspaceMember(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('member', 'Member'),
        ('viewer', 'Viewer'),
    ]
    
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workspace_memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_workspace_memberships')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_workspace_memberships')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('workspace', 'user')
        indexes = [
            models.Index(fields=['created_by']),
            models.Index(fields=['updated_by']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.workspace.name} ({self.role})"

class WorkspaceFolder(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='folders')
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subfolders')
    name = models.CharField(max_length=191)
    description = models.TextField(null=True, blank=True)
    path = models.CharField(max_length=191, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_workspace_folders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_workspace_folders')
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='deleted_workspace_folders')
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['workspace']),
            models.Index(fields=['parent_folder']),
            models.Index(fields=['path']),
            models.Index(fields=['created_by']),
            models.Index(fields=['updated_by']),
            models.Index(fields=['deleted_by']),
        ]

    def __str__(self):
        return f"{self.name} ({self.workspace.name})"

class WorkspaceDocument(models.Model):
    folder = models.ForeignKey(WorkspaceFolder, on_delete=models.CASCADE, related_name='documents')
    name = models.CharField(max_length=191)
    description = models.TextField(null=True, blank=True)
    file_path = models.CharField(max_length=191, null=True, blank=True)
    file_size = models.BigIntegerField(null=True)
    file_type = models.CharField(max_length=50, null=True)
    mime_type = models.CharField(max_length=100, null=True)
    version = models.IntegerField(default=1)
    is_locked = models.BooleanField(default=False)
    locked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='locked_workspace_documents')
    locked_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_workspace_documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_workspace_documents')
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='deleted_workspace_documents')
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['folder']),
            models.Index(fields=['name']),
            models.Index(fields=['file_type']),
            models.Index(fields=['is_locked']),
            models.Index(fields=['locked_by']),
            models.Index(fields=['created_by']),
            models.Index(fields=['updated_by']),
            models.Index(fields=['deleted_by']),
        ]

    def __str__(self):
        return f"{self.name} ({self.folder.name})"

class WorkspaceDocumentVersion(models.Model):
    document = models.ForeignKey(WorkspaceDocument, on_delete=models.CASCADE, related_name='versions')
    version = models.IntegerField()
    file_path = models.CharField(max_length=191, null=True)
    file_size = models.BigIntegerField(null=True)
    change_summary = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_workspace_document_versions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('document', 'version')
        indexes = [
            models.Index(fields=['document']),
            models.Index(fields=['created_by']),
        ]

    def __str__(self):
        return f"{self.document.name} - v{self.version}"

class WorkspaceDocumentPermission(models.Model):
    PERMISSION_CHOICES = [
        ('read', 'Read'),
        ('write', 'Write'),
        ('delete', 'Delete'),
        ('share', 'Share'),
    ]

    document = models.ForeignKey(WorkspaceDocument, on_delete=models.CASCADE, related_name='permissions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='workspace_document_permissions')
    group = models.ForeignKey('auth.Group', on_delete=models.CASCADE, null=True, related_name='workspace_document_permissions')
    permission_type = models.CharField(max_length=20, choices=PERMISSION_CHOICES)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_workspace_document_permissions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_workspace_document_permissions')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['document']),
            models.Index(fields=['user']),
            models.Index(fields=['group']),
            models.Index(fields=['created_by']),
            models.Index(fields=['updated_by']),
        ]

    def __str__(self):
        return f"{self.document.name} - {self.permission_type}"

class WorkspaceDocumentShare(models.Model):
    document = models.ForeignKey(WorkspaceDocument, on_delete=models.CASCADE, related_name='shares')
    share_token = models.CharField(max_length=191, unique=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    access_count = models.IntegerField(default=0)
    max_access_count = models.IntegerField(null=True, blank=True)
    permission_type = models.CharField(max_length=20, default='read')
    password_protected = models.BooleanField(default=False)
    password_hash = models.CharField(max_length=191, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_workspace_document_shares')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['document']),
            models.Index(fields=['expires_at']),
            models.Index(fields=['created_by']),
        ]

    def __str__(self):
        return f"{self.document.name} - {self.share_token}"

class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Created'),
        ('update', 'Updated'),
        ('delete', 'Deleted'),
        ('share', 'Shared'),
        ('unshare', 'Unshared'),
        ('lock', 'Locked'),
        ('unlock', 'Unlocked'),
        ('upload', 'Uploaded'),
        ('download', 'Downloaded'),
        ('comment', 'Commented'),
        ('move', 'Moved'),
        ('copy', 'Copied'),
        ('rename', 'Renamed'),
        ('restore', 'Restored'),
        ('archive', 'Archived'),
    ]

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='activities')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workspace_activities')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    target_type = models.CharField(max_length=50)  # e.g., 'document', 'folder', 'workspace'
    target_id = models.IntegerField()  # ID of the target object
    target_name = models.CharField(max_length=191)  # Name or description of the target
    details = models.TextField(null=True, blank=True)  # Additional details about the action
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['workspace']),
            models.Index(fields=['user']),
            models.Index(fields=['action']),
            models.Index(fields=['target_type']),
            models.Index(fields=['timestamp']),
        ]
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} {self.action} {self.target_type} '{self.target_name}' in {self.workspace.name}" 