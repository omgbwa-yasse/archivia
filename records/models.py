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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

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
