from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils import timezone

class WorkflowDefinition(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('active', 'Actif'),
        ('inactive', 'Inactif'),
    ]

    name = models.CharField(max_length=100, validators=[MinLengthValidator(3), MaxLengthValidator(100)])
    description = models.TextField(blank=True)
    bpmn_xml = models.TextField()
    version = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_workflow_definitions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_workflow_definitions')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Définition de workflow'
        verbose_name_plural = 'Définitions de workflows'

    def __str__(self):
        return f"{self.name} (v{self.version})"

class WorkflowInstance(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('active', 'Actif'),
        ('completed', 'Terminé'),
        ('cancelled', 'Annulé'),
    ]

    definition = models.ForeignKey(WorkflowDefinition, on_delete=models.PROTECT, related_name='instances')
    name = models.CharField(max_length=190, validators=[MinLengthValidator(3), MaxLengthValidator(190)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    current_state = models.JSONField()
    started_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='started_workflows')
    started_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_workflows')
    updated_at = models.DateTimeField(auto_now=True)
    completed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='completed_workflows')
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Instance de workflow'
        verbose_name_plural = 'Instances de workflows'

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminé'),
        ('cancelled', 'Annulé'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Basse'),
        ('medium', 'Moyenne'),
        ('high', 'Haute'),
        ('urgent', 'Urgente'),
    ]

    title = models.CharField(max_length=190, validators=[MinLengthValidator(3), MaxLengthValidator(190)])
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='assigned_workflow_tasks')
    workflow_instance = models.ForeignKey(WorkflowInstance, on_delete=models.SET_NULL, null=True, related_name='tasks')
    due_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_workflow_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_workflow_tasks')
    updated_at = models.DateTimeField(auto_now=True)
    completed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='completed_workflow_tasks')
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Tâche'
        verbose_name_plural = 'Tâches'

    def __str__(self):
        return self.title

    def complete(self, user):
        self.status = 'completed'
        self.completed_by = user
        self.completed_at = timezone.now()
        self.save()

    def is_overdue(self):
        return self.due_date and self.due_date < timezone.now() and self.status != 'completed' 