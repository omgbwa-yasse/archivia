from django.contrib import admin
from .models import (
    AIAgent, AIModel, AIAgentModel, AIPrompt, AIPromptVersion,
    AIChat, AIChatMessage, AIChatAttachment, AITool, AIAgentTool,
    AITask, AITaskResource, AITaskLog, AIUsageStat, AIReferenceData
)

@admin.register(AIAgent)
class AIAgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'status', 'version', 'created_by', 'created_at')
    list_filter = ('type', 'status', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'version', 'status', 'created_by')
    list_filter = ('provider', 'status', 'created_at')
    search_fields = ('name', 'version')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(AIAgentModel)
class AIAgentModelAdmin(admin.ModelAdmin):
    list_display = ('agent', 'model', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('agent__name', 'model__name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(AIPrompt)
class AIPromptAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(AIPromptVersion)
class AIPromptVersionAdmin(admin.ModelAdmin):
    list_display = ('prompt', 'version_number', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('prompt__title', 'comment')
    readonly_fields = ('created_at',)

@admin.register(AIChat)
class AIChatAdmin(admin.ModelAdmin):
    list_display = ('title', 'ai_agent', 'status', 'last_message_at', 'created_by')
    list_filter = ('status', 'created_at', 'last_message_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(AIChatMessage)
class AIChatMessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'role', 'message_order', 'tokens_input', 'tokens_output', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('chat__title', 'content')
    readonly_fields = ('created_at',)

@admin.register(AIChatAttachment)
class AIChatAttachmentAdmin(admin.ModelAdmin):
    list_display = ('message', 'file_name', 'file_type', 'file_size', 'created_at')
    list_filter = ('file_type', 'created_at')
    search_fields = ('file_name', 'file_path')
    readonly_fields = ('created_at',)

@admin.register(AITool)
class AIToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'version', 'status', 'created_by')
    list_filter = ('type', 'status', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(AIAgentTool)
class AIAgentToolAdmin(admin.ModelAdmin):
    list_display = ('agent', 'tool', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('agent__name', 'tool__name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(AITask)
class AITaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'agent', 'model', 'status', 'priority', 'created_by')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(AITaskResource)
class AITaskResourceAdmin(admin.ModelAdmin):
    list_display = ('task', 'resource_type', 'resource_name', 'processing_status', 'created_at')
    list_filter = ('resource_type', 'processing_status', 'created_at')
    search_fields = ('task__title', 'resource_name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(AITaskLog)
class AITaskLogAdmin(admin.ModelAdmin):
    list_display = ('task', 'level', 'created_at')
    list_filter = ('level', 'created_at')
    search_fields = ('task__name', 'message')
    readonly_fields = ('created_at',)

@admin.register(AIUsageStat)
class AIUsageStatAdmin(admin.ModelAdmin):
    list_display = ('user', 'usage_type', 'tokens_input', 'tokens_output', 'cost', 'created_at')
    list_filter = ('usage_type', 'success', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)

@admin.register(AIReferenceData)
class AIReferenceDataAdmin(admin.ModelAdmin):
    list_display = ('ai_agent', 'usage', 'created_by', 'created_at')
    list_filter = ('usage', 'created_at')
    search_fields = ('ai_agent__name',)
    readonly_fields = ('created_at',) 