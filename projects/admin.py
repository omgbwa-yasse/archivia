from django.contrib import admin
from .models import Project, ProjectMember, ProjectTask, ProjectResource, TaskDependency, TaskComment, TimeEntry

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'status', 'start_date', 'end_date', 'created_at')
    list_filter = ('status', 'owner', 'created_at')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at', 'deleted_at', 'version')

@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('project__name', 'user__username')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ProjectTask)
class ProjectTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'priority', 'assigned_to', 'due_date', 'created_at')
    list_filter = ('status', 'priority', 'project', 'created_at')
    search_fields = ('title', 'description', 'project__name')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at', 'deleted_at', 'version')

@admin.register(ProjectResource)
class ProjectResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'resource_type', 'quantity', 'unit_cost', 'created_at')
    list_filter = ('resource_type', 'project', 'created_at')
    search_fields = ('name', 'description', 'project__name')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at', 'deleted_at', 'version')

@admin.register(TaskDependency)
class TaskDependencyAdmin(admin.ModelAdmin):
    list_display = ('task', 'depends_on_task', 'dependency_type', 'created_at')
    list_filter = ('dependency_type', 'created_at')
    search_fields = ('task__title', 'depends_on_task__title')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)

@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('comment', 'task__title')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')

@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'hours_spent', 'work_date', 'created_at')
    list_filter = ('work_date', 'created_at')
    search_fields = ('task__title', 'user__username', 'description')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at') 