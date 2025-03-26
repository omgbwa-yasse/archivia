from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import AITask, AIChat, AIChatMessage

@receiver(pre_save, sender=AITask)
def update_task_duration(sender, instance, **kwargs):
    if instance.started_at and instance.completed_at:
        duration = (instance.completed_at - instance.started_at).total_seconds()
        instance.duration_seconds = int(duration)

@receiver(post_save, sender=AIChatMessage)
def update_chat_last_message(sender, instance, created, **kwargs):
    if created:
        instance.chat.last_message_at = timezone.now()
        instance.chat.save(update_fields=['last_message_at']) 