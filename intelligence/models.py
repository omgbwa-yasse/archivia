from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class AIAgent(models.Model):
    AGENT_TYPES = [
        ('GENERAL', 'General'),
        ('SPECIALIZED', 'Specialized'),
        ('CUSTOM', 'Custom'),
    ]
    
    AGENT_STATUS = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('MAINTENANCE', 'Maintenance'),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=AGENT_TYPES)
    configuration = models.JSONField(null=True, blank=True)
    system_prompt = models.TextField(null=True, blank=True)
    capabilities = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=AGENT_STATUS, default='ACTIVE')
    version = models.IntegerField(default=1)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_agents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_agents')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['type']),
            models.Index(fields=['status']),
            models.Index(fields=['created_by']),
            models.Index(fields=['updated_by']),
        ]

    def __str__(self):
        return self.name

    @property
    def status_color(self):
        status_colors = {
            'ACTIVE': 'success',
            'INACTIVE': 'secondary',
            'MAINTENANCE': 'warning',
        }
        return status_colors.get(self.status, 'secondary')

class AIModel(models.Model):
    MODEL_STATUS = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('DEPRECATED', 'Deprecated'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    provider = models.CharField(max_length=50)
    model_id = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=MODEL_STATUS, default='ACTIVE')
    capabilities = models.JSONField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_models')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_models')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['provider']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.provider} - {self.name}"

    @property
    def status_color(self):
        status_colors = {
            'ACTIVE': 'success',
            'INACTIVE': 'secondary',
            'DEPRECATED': 'warning',
        }
        return status_colors.get(self.status, 'secondary')

class AIAgentModel(models.Model):
    agent = models.ForeignKey(AIAgent, on_delete=models.CASCADE, related_name='agent_models')
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE, related_name='model_agents')
    is_primary = models.BooleanField(default=False)
    configuration = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['agent', 'model']
        indexes = [
            models.Index(fields=['agent']),
            models.Index(fields=['is_primary']),
        ]

    def __str__(self):
        return f"{self.agent.name} - {self.model.name}"

class AIPrompt(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    content = models.TextField()
    variables = models.JSONField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_prompts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_prompts')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class AIPromptVersion(models.Model):
    prompt = models.ForeignKey(AIPrompt, on_delete=models.CASCADE, related_name='versions')
    version_number = models.IntegerField()
    content = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_prompt_versions')
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ['prompt', 'version_number']
        indexes = [
            models.Index(fields=['created_by']),
        ]

    def __str__(self):
        return f"{self.prompt.name} v{self.version_number}"

class AIChat(models.Model):
    CHAT_STATUS = [
        ('ACTIVE', 'Active'),
        ('ARCHIVED', 'Archived'),
        ('DELETED', 'Deleted'),
    ]

    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    ai_agent = models.ForeignKey(AIAgent, on_delete=models.PROTECT, related_name='chats')
    chat_settings = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=CHAT_STATUS, default='ACTIVE')
    last_message_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_chats')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_chats')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['ai_agent']),
            models.Index(fields=['status']),
            models.Index(fields=['created_by']),
        ]

    def __str__(self):
        return self.title

    @property
    def status_color(self):
        status_colors = {
            'ACTIVE': 'success',
            'ARCHIVED': 'secondary',
            'DELETED': 'danger',
        }
        return status_colors.get(self.status, 'secondary')

class AIChatMessage(models.Model):
    MESSAGE_ROLES = [
        ('USER', 'User'),
        ('ASSISTANT', 'Assistant'),
        ('SYSTEM', 'System'),
    ]

    chat = models.ForeignKey(AIChat, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    role = models.CharField(max_length=20, choices=MESSAGE_ROLES)
    message_order = models.IntegerField()
    tokens_input = models.IntegerField(default=0)
    tokens_output = models.IntegerField(default=0)
    model = models.ForeignKey(AIModel, on_delete=models.SET_NULL, null=True, related_name='messages')
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['chat']),
            models.Index(fields=['message_order']),
            models.Index(fields=['role']),
            models.Index(fields=['model']),
        ]

    def __str__(self):
        return f"{self.chat.title} - {self.role} - {self.message_order}"

class AIChatAttachment(models.Model):
    message = models.ForeignKey(AIChatMessage, on_delete=models.CASCADE, related_name='attachments')
    file_path = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=100)
    file_size = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['message']),
            models.Index(fields=['file_type']),
        ]

    def __str__(self):
        return self.file_name

class AITool(models.Model):
    TOOL_TYPES = [
        ('EMAIL_PROCESSOR', 'Email Processor'),
        ('FILE_ANALYZER', 'File Analyzer'),
        ('PROJECT_MANAGER', 'Project Manager'),
        ('CODE_GENERATOR', 'Code Generator'),
        ('DATA_EXTRACTOR', 'Data Extractor'),
        ('CUSTOM', 'Custom'),
    ]

    TOOL_STATUS = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('DEPRECATED', 'Deprecated'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=TOOL_TYPES)
    capabilities = models.JSONField(null=True, blank=True)
    configuration = models.JSONField(null=True, blank=True)
    api_endpoint = models.CharField(max_length=255, null=True, blank=True)
    version = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=TOOL_STATUS, default='ACTIVE')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_tools')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_tools')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['name', 'version']
        indexes = [
            models.Index(fields=['type']),
            models.Index(fields=['status']),
            models.Index(fields=['created_by']),
        ]

    def __str__(self):
        return f"{self.name} v{self.version}"

class AIAgentTool(models.Model):
    agent = models.ForeignKey(AIAgent, on_delete=models.CASCADE, related_name='agent_tools')
    tool = models.ForeignKey(AITool, on_delete=models.CASCADE, related_name='tool_agents')
    configuration = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['agent', 'tool']

    def __str__(self):
        return f"{self.agent.name} - {self.tool.name}"

class AITask(models.Model):
    TASK_STATUS = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]

    TASK_PRIORITY = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    agent = models.ForeignKey(AIAgent, on_delete=models.PROTECT, related_name='tasks')
    model = models.ForeignKey(AIModel, on_delete=models.PROTECT, related_name='tasks')
    prompt = models.ForeignKey(AIPrompt, on_delete=models.PROTECT, related_name='tasks')
    status = models.CharField(max_length=20, choices=TASK_STATUS, default='PENDING')
    priority = models.CharField(max_length=20, choices=TASK_PRIORITY, default='MEDIUM')
    input_data = models.JSONField(null=True, blank=True)
    output_data = models.JSONField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_ai_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_ai_tasks')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['agent']),
            models.Index(fields=['model']),
            models.Index(fields=['created_by']),
        ]

    def __str__(self):
        return self.name

    @property
    def status_color(self):
        status_colors = {
            'PENDING': 'secondary',
            'PROCESSING': 'info',
            'COMPLETED': 'success',
            'FAILED': 'danger',
            'CANCELLED': 'warning',
        }
        return status_colors.get(self.status, 'secondary')

    @property
    def priority_color(self):
        priority_colors = {
            'LOW': 'success',
            'MEDIUM': 'info',
            'HIGH': 'warning',
            'URGENT': 'danger',
        }
        return priority_colors.get(self.priority, 'info')

    def start(self):
        self.status = 'PROCESSING'
        self.started_at = timezone.now()
        self.save()

    def complete(self, output_data=None):
        self.status = 'COMPLETED'
        self.completed_at = timezone.now()
        if output_data is not None:
            self.output_data = output_data
        self.save()

    def fail(self, error_message):
        self.status = 'FAILED'
        self.completed_at = timezone.now()
        self.error_message = error_message
        self.save()

    def cancel(self):
        self.status = 'CANCELLED'
        self.completed_at = timezone.now()
        self.save()

class AITaskResult(models.Model):
    task = models.ForeignKey(AITask, on_delete=models.CASCADE, related_name='results')
    result_type = models.CharField(max_length=50)
    content = models.JSONField()
    confidence_score = models.FloatField(null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['task']),
            models.Index(fields=['result_type']),
        ]

    def __str__(self):
        return f"{self.task.name} - {self.result_type}"

class AITaskLog(models.Model):
    LOG_LEVELS = [
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('DEBUG', 'Debug'),
    ]

    task = models.ForeignKey(AITask, on_delete=models.CASCADE, related_name='logs')
    level = models.CharField(max_length=10, choices=LOG_LEVELS)
    message = models.TextField()
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['task']),
            models.Index(fields=['level']),
        ]

    def __str__(self):
        return f"{self.task.name} - {self.level}"

class AITaskFeedback(models.Model):
    FEEDBACK_TYPES = [
        ('POSITIVE', 'Positive'),
        ('NEGATIVE', 'Negative'),
        ('NEUTRAL', 'Neutral'),
    ]

    task = models.ForeignKey(AITask, on_delete=models.CASCADE, related_name='feedback')
    feedback_type = models.CharField(max_length=10, choices=FEEDBACK_TYPES)
    comment = models.TextField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='given_feedback')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['task']),
            models.Index(fields=['feedback_type']),
        ]

    def __str__(self):
        return f"{self.task.name} - {self.feedback_type}"

class AITaskResource(models.Model):
    RESOURCE_TYPES = [
        ('EMAIL', 'Email'),
        ('FILE', 'File'),
        ('FOLDER', 'Folder'),
        ('PROJECT', 'Project'),
        ('WORKSPACE', 'Workspace'),
        ('DATABASE', 'Database'),
        ('API', 'API'),
        ('DOCUMENT', 'Document'),
        ('CODE', 'Code'),
        ('OTHER', 'Other'),
    ]

    PROCESSING_STATUS = [
        ('PENDING', 'Pending'),
        ('PROCESSED', 'Processed'),
        ('FAILED', 'Failed'),
        ('SKIPPED', 'Skipped'),
    ]

    task = models.ForeignKey(AITask, on_delete=models.CASCADE, related_name='resources')
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    resource_id = models.BigIntegerField(null=True, blank=True)
    resource_path = models.CharField(max_length=255, null=True, blank=True)
    resource_name = models.CharField(max_length=255)
    resource_metadata = models.JSONField(null=True, blank=True)
    is_input = models.BooleanField(default=True)
    is_output = models.BooleanField(default=False)
    processing_status = models.CharField(max_length=20, choices=PROCESSING_STATUS, default='PENDING')
    processing_result = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['task']),
            models.Index(fields=['resource_type']),
            models.Index(fields=['processing_status']),
        ]

    def __str__(self):
        return f"{self.task.name} - {self.resource_name}"

class AIUsageStat(models.Model):
    USAGE_TYPES = [
        ('CHAT', 'Chat'),
        ('TASK', 'Task'),
        ('PROMPT', 'Prompt'),
        ('TOOL_CALL', 'Tool Call'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='ai_usage')
    ai_agent = models.ForeignKey(AIAgent, on_delete=models.SET_NULL, null=True, blank=True, related_name='usage_stats')
    ai_model = models.ForeignKey(AIModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='usage_stats')
    ai_tool = models.ForeignKey(AITool, on_delete=models.SET_NULL, null=True, blank=True, related_name='usage_stats')
    usage_type = models.CharField(max_length=20, choices=USAGE_TYPES)
    task = models.ForeignKey(AITask, on_delete=models.SET_NULL, null=True, blank=True, related_name='usage_stats')
    resource_id = models.BigIntegerField(null=True, blank=True)
    tokens_input = models.IntegerField(default=0)
    tokens_output = models.IntegerField(default=0)
    duration_ms = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    success = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
            models.Index(fields=['ai_agent']),
            models.Index(fields=['ai_model']),
            models.Index(fields=['task']),
            models.Index(fields=['usage_type']),
            models.Index(fields=['success']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.usage_type} - {self.created_at}"

    @property
    def duration_seconds(self):
        """Retourne la durée en secondes"""
        return self.duration_ms / 1000 if self.duration_ms else 0

class AIReferenceData(models.Model):
    USAGE_TYPES = [
        ('TRAINING', 'Training'),
        ('REFERENCE', 'Reference'),
        ('FINE_TUNING', 'Fine Tuning'),
        ('CONTEXT', 'Context'),
    ]

    ai_agent = models.ForeignKey(AIAgent, on_delete=models.CASCADE, related_name='reference_data')
    usage = models.CharField(max_length=20, choices=USAGE_TYPES)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_ai_references')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['ai_agent', 'usage']
        indexes = [
            models.Index(fields=['ai_agent']),
        ]

    def __str__(self):
        return f"{self.ai_agent.name} - {self.usage}" 