from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth import get_user_model
from tools.models import Activity

User = get_user_model()

class Folder(models.Model):
    name = models.CharField(_('Name'), max_length=190)
    description = models.TextField(_('Description'), blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_folders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_folders')
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='deleted_folders')
    deleted_at = models.DateTimeField(null=True, blank=True)
    version = models.IntegerField(default=1)
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _('Folder')
        verbose_name_plural = _('Folders')
        ordering = ['name']

    def __str__(self):
        return self.name

    def soft_delete(self, user):
        self.deleted_by = user
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_by = None
        self.deleted_at = None
        self.save()

class Document(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/')
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='documents')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    retention = models.ForeignKey('Retention', on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    document_metadata = models.JSONField(default=dict)
    favorite_users = models.ManyToManyField(User, through='Favorite', related_name='favorite_documents')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['created_at']),
            models.Index(fields=['deleted_at']),
        ]

    def __str__(self):
        return self.name

    def soft_delete(self, user):
        self.deleted_at = timezone.now()
        self.save()
        AuditLog.objects.create(
            action='delete',
            model='Document',
            object_id=self.id,
            user=user,
            details=f'Document "{self.name}" soft deleted'
        )

    def restore(self):
        self.deleted_at = None
        self.save()
        AuditLog.objects.create(
            action='restore',
            model='Document',
            object_id=self.id,
            user=self.created_by,
            details=f'Document "{self.name}" restored'
        )

    def hard_delete(self):
        self.file.delete(save=False)
        self.delete()

    @property
    def is_deleted(self):
        return self.deleted_at is not None

class MetadataDefinition(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    description = models.TextField(_('Description'), blank=True, null=True)
    data_type = models.CharField(_('Data Type'), max_length=20)
    mandatory = models.BooleanField(_('Mandatory'), default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_metadata_definitions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_metadata_definitions')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Metadata Definition')
        verbose_name_plural = _('Metadata Definitions')
        ordering = ['name']

    def __str__(self):
        return self.name

class DocumentMetadata(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='metadata')
    definition = models.ForeignKey(MetadataDefinition, on_delete=models.CASCADE)
    value = models.TextField(_('Value'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_document_metadata')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_document_metadata')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Document Metadata')
        verbose_name_plural = _('Document Metadata')
        unique_together = ['document', 'definition']

    def __str__(self):
        return f"{self.document.name} - {self.definition.name}"

class FolderMetadata(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='metadata')
    definition = models.ForeignKey(MetadataDefinition, on_delete=models.CASCADE)
    value = models.TextField(_('Value'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_folder_metadata')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_folder_metadata')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Folder Metadata')
        verbose_name_plural = _('Folder Metadata')
        unique_together = ['folder', 'definition']

    def __str__(self):
        return f"{self.folder.name} - {self.definition.name}"

class ReferenceList(models.Model):
    name = models.CharField(_('Name'), max_length=100, unique=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_reference_lists')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_reference_lists')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Reference List')
        verbose_name_plural = _('Reference Lists')
        ordering = ['name']

    def __str__(self):
        return self.name

class ReferenceValue(models.Model):
    list = models.ForeignKey(ReferenceList, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(_('Value'), max_length=190)
    description = models.TextField(_('Description'), blank=True, null=True)
    active = models.BooleanField(_('Active'), default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_reference_values')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_reference_values')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Reference Value')
        verbose_name_plural = _('Reference Values')
        ordering = ['value']
        unique_together = ['list', 'value']

    def __str__(self):
        return f"{self.list.name} - {self.value}"

class Category(models.Model):
    name = models.CharField(_('Name'), max_length=100, unique=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_categories')
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='deleted_categories')
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']

    def __str__(self):
        return self.name

    def soft_delete(self, user):
        self.deleted_by = user
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_by = None
        self.deleted_at = None
        self.save()

class Archive(models.Model):
    name = models.CharField(_('Name'), max_length=190)
    description = models.TextField(_('Description'), blank=True, null=True)
    location = models.CharField(_('Location'), max_length=255)
    capacity = models.IntegerField(_('Capacity'), help_text=_('Capacity in cubic meters'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_archives')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_archives')
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='deleted_archives')
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Archive')
        verbose_name_plural = _('Archives')
        ordering = ['name']

    def __str__(self):
        return self.name

    def soft_delete(self, user):
        self.deleted_by = user
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_by = None
        self.deleted_at = None
        self.save()

class Retention(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    retention_period = models.IntegerField()  # in days
    retention_type = models.CharField(max_length=50)
    created_by = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='records_created_retentions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey('users.User', on_delete=models.PROTECT, null=True, blank=True, related_name='records_updated_retentions')
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.ForeignKey('users.User', on_delete=models.PROTECT, null=True, blank=True, related_name='records_deleted_retentions')
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Retention'
        verbose_name_plural = 'Retentions'

    def __str__(self):
        return self.name

class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(_('Action'), max_length=50)
    model = models.CharField(_('Model'), max_length=50)
    object_id = models.IntegerField(_('Object ID'))
    details = models.TextField(_('Details'), blank=True)
    timestamp = models.DateTimeField(_('Timestamp'), auto_now_add=True)
    ip_address = models.GenericIPAddressField(_('IP Address'), null=True, blank=True)

    class Meta:
        verbose_name = _('Audit Log')
        verbose_name_plural = _('Audit Logs')
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} - {self.action} - {self.model} - {self.timestamp}"

class AccessLog(models.Model):
    """Model for tracking document access."""
    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name='access_logs')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    accessed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-accessed_at']
        verbose_name = 'Access Log'
        verbose_name_plural = 'Access Logs'
    
    def __str__(self):
        return f"{self.user} accessed {self.document} at {self.accessed_at}"

class Favorite(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='favorite_entries')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_entries')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['document', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.document.name}"
