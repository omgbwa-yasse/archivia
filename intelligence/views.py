from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import (
    AIAgent, AIModel, AIPrompt, AIPromptVersion,
    AIChat, AIChatMessage, AIChatAttachment, AITool,
    AITask, AITaskResource, AITaskLog, AIUsageStat,
    AIReferenceData
)
from .forms import (
    AIAgentForm, AIModelForm, AIPromptForm, AIChatForm,
    AIToolForm, AITaskForm, AIReferenceDataForm
)

# AI Agent Views
class AIAgentListView(LoginRequiredMixin, ListView):
    model = AIAgent
    template_name = 'intelligence/agent_list.html'
    context_object_name = 'agents'

class AIAgentCreateView(LoginRequiredMixin, CreateView):
    model = AIAgent
    form_class = AIAgentForm
    template_name = 'intelligence/agent_form.html'
    success_url = reverse_lazy('intelligence:agent_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class AIAgentDetailView(LoginRequiredMixin, DetailView):
    model = AIAgent
    template_name = 'intelligence/agent_detail.html'
    context_object_name = 'agent'

class AIAgentUpdateView(LoginRequiredMixin, UpdateView):
    model = AIAgent
    form_class = AIAgentForm
    template_name = 'intelligence/agent_form.html'
    success_url = reverse_lazy('intelligence:agent_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class AIAgentDeleteView(LoginRequiredMixin, DeleteView):
    model = AIAgent
    template_name = 'intelligence/agent_confirm_delete.html'
    success_url = reverse_lazy('intelligence:agent_list')

# AI Model Views
class AIModelListView(LoginRequiredMixin, ListView):
    model = AIModel
    template_name = 'intelligence/model_list.html'
    context_object_name = 'models'

class AIModelCreateView(LoginRequiredMixin, CreateView):
    model = AIModel
    form_class = AIModelForm
    template_name = 'intelligence/model_form.html'
    success_url = reverse_lazy('intelligence:model_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class AIModelDetailView(LoginRequiredMixin, DetailView):
    model = AIModel
    template_name = 'intelligence/model_detail.html'
    context_object_name = 'model'

class AIModelUpdateView(LoginRequiredMixin, UpdateView):
    model = AIModel
    form_class = AIModelForm
    template_name = 'intelligence/model_form.html'
    success_url = reverse_lazy('intelligence:model_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class AIModelDeleteView(LoginRequiredMixin, DeleteView):
    model = AIModel
    template_name = 'intelligence/model_confirm_delete.html'
    success_url = reverse_lazy('intelligence:model_list')

# AI Prompt Views
class AIPromptListView(LoginRequiredMixin, ListView):
    model = AIPrompt
    template_name = 'intelligence/prompt_list.html'
    context_object_name = 'prompts'

class AIPromptCreateView(LoginRequiredMixin, CreateView):
    model = AIPrompt
    form_class = AIPromptForm
    template_name = 'intelligence/prompt_form.html'
    success_url = reverse_lazy('intelligence:prompt_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class AIPromptDetailView(LoginRequiredMixin, DetailView):
    model = AIPrompt
    template_name = 'intelligence/prompt_detail.html'
    context_object_name = 'prompt'

class AIPromptUpdateView(LoginRequiredMixin, UpdateView):
    model = AIPrompt
    form_class = AIPromptForm
    template_name = 'intelligence/prompt_form.html'
    success_url = reverse_lazy('intelligence:prompt_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class AIPromptDeleteView(LoginRequiredMixin, DeleteView):
    model = AIPrompt
    template_name = 'intelligence/prompt_confirm_delete.html'
    success_url = reverse_lazy('intelligence:prompt_list')

class AIPromptVersionListView(LoginRequiredMixin, ListView):
    model = AIPromptVersion
    template_name = 'intelligence/prompt_version_list.html'
    context_object_name = 'versions'

    def get_queryset(self):
        return AIPromptVersion.objects.filter(prompt_id=self.kwargs['pk'])

# AI Chat Views
class AIChatListView(LoginRequiredMixin, ListView):
    model = AIChat
    template_name = 'intelligence/chat_list.html'
    context_object_name = 'chats'

    def get_queryset(self):
        return AIChat.objects.filter(user=self.request.user)

class AIChatCreateView(LoginRequiredMixin, CreateView):
    model = AIChat
    form_class = AIChatForm
    template_name = 'intelligence/chat_form.html'
    success_url = reverse_lazy('intelligence:chat_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AIChatDetailView(LoginRequiredMixin, DetailView):
    model = AIChat
    template_name = 'intelligence/chat_detail.html'
    context_object_name = 'chat'

class AIChatUpdateView(LoginRequiredMixin, UpdateView):
    model = AIChat
    form_class = AIChatForm
    template_name = 'intelligence/chat_form.html'
    success_url = reverse_lazy('intelligence:chat_list')

class AIChatDeleteView(LoginRequiredMixin, DeleteView):
    model = AIChat
    template_name = 'intelligence/chat_confirm_delete.html'
    success_url = reverse_lazy('intelligence:chat_list')

@require_POST
def chat_archive(request, pk):
    chat = get_object_or_404(AIChat, pk=pk, user=request.user)
    chat.is_archived = True
    chat.save()
    messages.success(request, "Le chat a été archivé avec succès.")
    return redirect('intelligence:chat_list')

class AIChatMessageListView(LoginRequiredMixin, ListView):
    model = AIChatMessage
    template_name = 'intelligence/chat_message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return AIChatMessage.objects.filter(chat_id=self.kwargs['pk'])

class AIChatMessageCreateView(LoginRequiredMixin, CreateView):
    model = AIChatMessage
    template_name = 'intelligence/chat_message_form.html'
    fields = ['content']
    success_url = reverse_lazy('intelligence:chat_detail')

    def form_valid(self, form):
        form.instance.chat_id = self.kwargs['pk']
        form.instance.role = 'user'
        return super().form_valid(form)

# AI Tool Views
class AIToolListView(LoginRequiredMixin, ListView):
    model = AITool
    template_name = 'intelligence/tool_list.html'
    context_object_name = 'tools'

class AIToolCreateView(LoginRequiredMixin, CreateView):
    model = AITool
    form_class = AIToolForm
    template_name = 'intelligence/tool_form.html'
    success_url = reverse_lazy('intelligence:tool_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class AIToolDetailView(LoginRequiredMixin, DetailView):
    model = AITool
    template_name = 'intelligence/tool_detail.html'
    context_object_name = 'tool'

class AIToolUpdateView(LoginRequiredMixin, UpdateView):
    model = AITool
    form_class = AIToolForm
    template_name = 'intelligence/tool_form.html'
    success_url = reverse_lazy('intelligence:tool_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class AIToolDeleteView(LoginRequiredMixin, DeleteView):
    model = AITool
    template_name = 'intelligence/tool_confirm_delete.html'
    success_url = reverse_lazy('intelligence:tool_list')

# AI Task Views
class AITaskListView(LoginRequiredMixin, ListView):
    model = AITask
    template_name = 'intelligence/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return AITask.objects.filter(user=self.request.user)

class AITaskCreateView(LoginRequiredMixin, CreateView):
    model = AITask
    form_class = AITaskForm
    template_name = 'intelligence/task_form.html'
    success_url = reverse_lazy('intelligence:task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AITaskDetailView(LoginRequiredMixin, DetailView):
    model = AITask
    template_name = 'intelligence/task_detail.html'
    context_object_name = 'task'

class AITaskUpdateView(LoginRequiredMixin, UpdateView):
    model = AITask
    form_class = AITaskForm
    template_name = 'intelligence/task_form.html'
    success_url = reverse_lazy('intelligence:task_list')

class AITaskDeleteView(LoginRequiredMixin, DeleteView):
    model = AITask
    template_name = 'intelligence/task_confirm_delete.html'
    success_url = reverse_lazy('intelligence:task_list')

@require_POST
def task_start(request, pk):
    task = get_object_or_404(AITask, pk=pk, user=request.user)
    task.status = 'RUNNING'
    task.save()
    return JsonResponse({'status': 'success'})

@require_POST
def task_complete(request, pk):
    task = get_object_or_404(AITask, pk=pk, user=request.user)
    task.status = 'COMPLETED'
    task.completed_at = timezone.now()
    task.save()
    return JsonResponse({'status': 'success'})

@require_POST
def task_fail(request, pk):
    task = get_object_or_404(AITask, pk=pk, user=request.user)
    task.status = 'FAILED'
    task.failed_at = timezone.now()
    task.save()
    return JsonResponse({'status': 'success'})

@require_POST
def task_cancel(request, pk):
    task = get_object_or_404(AITask, pk=pk, user=request.user)
    task.status = 'CANCELLED'
    task.cancelled_at = timezone.now()
    task.save()
    return JsonResponse({'status': 'success'})

class AITaskFeedbackCreateView(LoginRequiredMixin, CreateView):
    model = AITaskLog
    template_name = 'intelligence/task_feedback_form.html'
    fields = ['message', 'level']
    success_url = reverse_lazy('intelligence:task_detail')

    def form_valid(self, form):
        form.instance.task_id = self.kwargs['pk']
        form.instance.level = 'FEEDBACK'
        return super().form_valid(form)

# AI Usage Stats Views
class AIUsageStatListView(LoginRequiredMixin, ListView):
    model = AIUsageStat
    template_name = 'intelligence/usage_stats_list.html'
    context_object_name = 'stats'

    def get_queryset(self):
        return AIUsageStat.objects.filter(user=self.request.user)

def usage_stats_export(request):
    stats = AIUsageStat.objects.filter(user=request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="usage_stats.csv"'
    # TODO: Implement CSV export
    return response

# AI Reference Data Views
class AIReferenceDataListView(LoginRequiredMixin, ListView):
    model = AIReferenceData
    template_name = 'intelligence/reference_data_list.html'
    context_object_name = 'references'

class AIReferenceDataCreateView(LoginRequiredMixin, CreateView):
    model = AIReferenceData
    form_class = AIReferenceDataForm
    template_name = 'intelligence/reference_data_form.html'
    success_url = reverse_lazy('intelligence:reference_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class AIReferenceDataDetailView(LoginRequiredMixin, DetailView):
    model = AIReferenceData
    template_name = 'intelligence/reference_data_detail.html'
    context_object_name = 'reference'

class AIReferenceDataUpdateView(LoginRequiredMixin, UpdateView):
    model = AIReferenceData
    form_class = AIReferenceDataForm
    template_name = 'intelligence/reference_data_form.html'
    success_url = reverse_lazy('intelligence:reference_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class AIReferenceDataDeleteView(LoginRequiredMixin, DeleteView):
    model = AIReferenceData
    template_name = 'intelligence/reference_data_confirm_delete.html'
    success_url = reverse_lazy('intelligence:reference_list') 