from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Workspace, WorkspaceFolder, WorkspaceDocument

@receiver(pre_save, sender=WorkspaceFolder)
def update_folder_path(sender, instance, **kwargs):
    """Update the folder path when saving a workspace folder."""
    if instance.parent_folder:
        instance.path = f"{instance.parent_folder.path}/{instance.name}"
    else:
        instance.path = instance.name

@receiver(post_save, sender=Workspace)
def create_root_folder(sender, instance, created, **kwargs):
    """Create a root folder when a new workspace is created."""
    if created:
        WorkspaceFolder.objects.create(
            workspace=instance,
            name='Root',
            created_by=instance.created_by
        )

@receiver(pre_save, sender=WorkspaceDocument)
def handle_document_lock(sender, instance, **kwargs):
    """Handle document locking logic."""
    if instance.is_locked and not instance.locked_at:
        instance.locked_at = timezone.now()
    elif not instance.is_locked:
        instance.locked_at = None
        instance.locked_by = None 