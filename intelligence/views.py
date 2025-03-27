from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
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
from django.db import models

@login_required
def dashboard(request):
    context = {
        'agents_count': AIAgent.objects.count(),
        'models_count': AIModel.objects.count(),
        'tasks_count': AITask.objects.filter(created_by=request.user).count(),
        'chats_count': AIChat.objects.filter(created_by=request.user).count(),
    }
    return render(request, 'intelligence/dashboard.html', context)

@login_required
def analysis(request):
    return render(request, 'intelligence/analysis.html')

@login_required
def predictions(request):
    return render(request, 'intelligence/predictions.html')

@login_required
def training(request):
    return render(request, 'intelligence/training.html')

@login_required
def evaluation(request):
    return render(request, 'intelligence/evaluation.html')

# AI Agent Views
class AIAgentListView(LoginRequiredMixin, ListView):
    model = AIAgent
    template_name = 'intelligence/agent/agent_list.html'
    context_object_name = 'agents'

class AIAgentCreateView(LoginRequiredMixin, CreateView):
    model = AIAgent
    form_class = AIAgentForm
    template_name = 'intelligence/agent/agent_form.html'
    success_url = reverse_lazy('intelligence:agent_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class AIAgentDetailView(LoginRequiredMixin, DetailView):
    model = AIAgent
    template_name = 'intelligence/agent/agent_detail.html'
    context_object_name = 'agent'

class AIAgentUpdateView(LoginRequiredMixin, UpdateView):
    model = AIAgent
    form_class = AIAgentForm
    template_name = 'intelligence/agent/agent_form.html'
    success_url = reverse_lazy('intelligence:agent_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class AIAgentDeleteView(LoginRequiredMixin, DeleteView):
    model = AIAgent
    template_name = 'intelligence/agent/agent_confirm_delete.html'
    success_url = reverse_lazy('intelligence:agent_list')

# AI Model Views
class AIModelListView(LoginRequiredMixin, ListView):
    model = AIModel
    template_name = 'intelligence/model/model_list.html'
    context_object_name = 'models'

class AIModelCreateView(LoginRequiredMixin, CreateView):
    model = AIModel
    form_class = AIModelForm
    template_name = 'intelligence/model/model_form.html'
    success_url = reverse_lazy('intelligence:model_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class AIModelDetailView(LoginRequiredMixin, DetailView):
    model = AIModel
    template_name = 'intelligence/model/model_detail.html'
    context_object_name = 'model'

class AIModelUpdateView(LoginRequiredMixin, UpdateView):
    model = AIModel
    form_class = AIModelForm
    template_name = 'intelligence/model/model_form.html'
    success_url = reverse_lazy('intelligence:model_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class AIModelDeleteView(LoginRequiredMixin, DeleteView):
    model = AIModel
    template_name = 'intelligence/model/model_confirm_delete.html'
    success_url = reverse_lazy('intelligence:model_list')

# AI Prompt Views
class AIPromptListView(LoginRequiredMixin, ListView):
    model = AIPrompt
    template_name = 'intelligence/prompt/prompt_list.html'
    context_object_name = 'prompts'

class AIPromptCreateView(LoginRequiredMixin, CreateView):
    model = AIPrompt
    form_class = AIPromptForm
    template_name = 'intelligence/prompt/prompt_form.html'
    success_url = reverse_lazy('intelligence:prompt_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class AIPromptDetailView(LoginRequiredMixin, DetailView):
    model = AIPrompt
    template_name = 'intelligence/prompt/prompt_detail.html'
    context_object_name = 'prompt'

class AIPromptUpdateView(LoginRequiredMixin, UpdateView):
    model = AIPrompt
    form_class = AIPromptForm
    template_name = 'intelligence/prompt/prompt_form.html'
    success_url = reverse_lazy('intelligence:prompt_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class AIPromptDeleteView(LoginRequiredMixin, DeleteView):
    model = AIPrompt
    template_name = 'intelligence/prompt/prompt_confirm_delete.html'
    success_url = reverse_lazy('intelligence:prompt_list')

class AIPromptVersionListView(LoginRequiredMixin, ListView):
    model = AIPromptVersion
    template_name = 'intelligence/prompt/prompt_versions.html'
    context_object_name = 'versions'

    def get_queryset(self):
        return AIPromptVersion.objects.filter(prompt_id=self.kwargs['pk'])

# AI Chat Views
class AIChatListView(LoginRequiredMixin, ListView):
    model = AIChat
    template_name = 'intelligence/chat/chat_list.html'
    context_object_name = 'chats'

    def get_queryset(self):
        return AIChat.objects.filter(created_by=self.request.user)

class AIChatCreateView(LoginRequiredMixin, CreateView):
    model = AIChat
    form_class = AIChatForm
    template_name = 'intelligence/chat/chat_form.html'
    success_url = reverse_lazy('intelligence:chat_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class AIChatDetailView(LoginRequiredMixin, DetailView):
    model = AIChat
    template_name = 'intelligence/chat/chat_detail.html'
    context_object_name = 'chat'

class AIChatUpdateView(LoginRequiredMixin, UpdateView):
    model = AIChat
    form_class = AIChatForm
    template_name = 'intelligence/chat/chat_form.html'
    success_url = reverse_lazy('intelligence:chat_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class AIChatDeleteView(LoginRequiredMixin, DeleteView):
    model = AIChat
    template_name = 'intelligence/chat/chat_confirm_delete.html'
    success_url = reverse_lazy('intelligence:chat_list')

@require_POST
def chat_archive(request, pk):
    chat = get_object_or_404(AIChat, pk=pk, created_by=request.user)
    chat.is_archived = True
    chat.save()
    messages.success(request, "Le chat a été archivé avec succès.")
    return redirect('intelligence:chat_list')

class AIChatMessageListView(LoginRequiredMixin, ListView):
    model = AIChatMessage
    template_name = 'intelligence/chat/chat_message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return AIChatMessage.objects.filter(chat_id=self.kwargs['pk'])

class AIChatMessageCreateView(LoginRequiredMixin, CreateView):
    model = AIChatMessage
    template_name = 'intelligence/chat/chat_message_form.html'
    fields = ['content']
    success_url = reverse_lazy('intelligence:chat_detail')

    def form_valid(self, form):
        form.instance.chat_id = self.kwargs['pk']
        form.instance.role = 'user'
        return super().form_valid(form)

# AI Tool Views
class AIToolListView(LoginRequiredMixin, ListView):
    model = AITool
    template_name = 'intelligence/tool/tool_list.html'
    context_object_name = 'tools'

class AIToolCreateView(LoginRequiredMixin, CreateView):
    model = AITool
    form_class = AIToolForm
    template_name = 'intelligence/tool/tool_form.html'
    success_url = reverse_lazy('intelligence:tool_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class AIToolDetailView(LoginRequiredMixin, DetailView):
    model = AITool
    template_name = 'intelligence/tool/tool_detail.html'
    context_object_name = 'tool'

class AIToolUpdateView(LoginRequiredMixin, UpdateView):
    model = AITool
    form_class = AIToolForm
    template_name = 'intelligence/tool/tool_form.html'
    success_url = reverse_lazy('intelligence:tool_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class AIToolDeleteView(LoginRequiredMixin, DeleteView):
    model = AITool
    template_name = 'intelligence/tool/tool_confirm_delete.html'
    success_url = reverse_lazy('intelligence:tool_list')

# AI Task Views
class AITaskListView(LoginRequiredMixin, ListView):
    model = AITask
    template_name = 'intelligence/task/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return AITask.objects.filter(created_by=self.request.user)

class AITaskCreateView(LoginRequiredMixin, CreateView):
    model = AITask
    form_class = AITaskForm
    template_name = 'intelligence/task/task_form.html'
    success_url = reverse_lazy('intelligence:task_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class AITaskDetailView(LoginRequiredMixin, DetailView):
    model = AITask
    template_name = 'intelligence/task/task_detail.html'
    context_object_name = 'task'

class AITaskUpdateView(LoginRequiredMixin, UpdateView):
    model = AITask
    form_class = AITaskForm
    template_name = 'intelligence/task/task_form.html'
    success_url = reverse_lazy('intelligence:task_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class AITaskDeleteView(LoginRequiredMixin, DeleteView):
    model = AITask
    template_name = 'intelligence/task/task_confirm_delete.html'
    success_url = reverse_lazy('intelligence:task_list')

class AITaskResourceListView(LoginRequiredMixin, ListView):
    model = AITaskResource
    template_name = 'intelligence/task/task_resource_list.html'
    context_object_name = 'resources'

    def get_queryset(self):
        return AITaskResource.objects.filter(task_id=self.kwargs['pk'])

class AITaskLogListView(LoginRequiredMixin, ListView):
    model = AITaskLog
    template_name = 'intelligence/task/task_log_list.html'
    context_object_name = 'logs'

    def get_queryset(self):
        return AITaskLog.objects.filter(task_id=self.kwargs['pk'])

@require_POST
def task_start(request, pk):
    task = get_object_or_404(AITask, pk=pk, created_by=request.user)
    task.start()
    return JsonResponse({'status': 'success'})

@require_POST
def task_complete(request, pk):
    task = get_object_or_404(AITask, pk=pk, created_by=request.user)
    task.complete()
    return JsonResponse({'status': 'success'})

@require_POST
def task_fail(request, pk):
    task = get_object_or_404(AITask, pk=pk, created_by=request.user)
    task.fail()
    return JsonResponse({'status': 'success'})

@require_POST
def task_cancel(request, pk):
    task = get_object_or_404(AITask, pk=pk, created_by=request.user)
    task.cancel()
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
    paginate_by = 20

    def get_queryset(self):
        queryset = AIUsageStat.objects.all().order_by('-created_at')
        
        # Filtres
        usage_type = self.request.GET.get('usage_type')
        success = self.request.GET.get('success')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if usage_type:
            queryset = queryset.filter(usage_type=usage_type)
        if success is not None:
            queryset = queryset.filter(success=success == 'true')
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        # Statistiques globales
        context['total_usage'] = queryset.count()
        context['total_tokens'] = queryset.aggregate(
            total=models.Sum(models.F('tokens_input') + models.F('tokens_output'))
        )['total'] or 0
        context['total_cost'] = queryset.aggregate(
            total=models.Sum('cost')
        )['total'] or 0

        # Calcul du taux de succès
        total_success = queryset.filter(success=True).count()
        context['success_rate'] = round(
            (total_success / context['total_usage'] * 100) if context['total_usage'] > 0 else 0
        )

        # Types d'utilisation pour le filtre
        context['usage_types'] = AIUsageStat.USAGE_TYPES

        return context

def usage_stats_export(request):
    stats = AIUsageStat.objects.filter(user=request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="usage_stats.csv"'
    # TODO: Implement CSV export
    return response

# AI Reference Data Views
class AIReferenceDataListView(LoginRequiredMixin, ListView):
    model = AIReferenceData
    template_name = 'intelligence/reference/reference_list.html'
    context_object_name = 'references'

class AIReferenceDataCreateView(LoginRequiredMixin, CreateView):
    model = AIReferenceData
    form_class = AIReferenceDataForm
    template_name = 'intelligence/reference/reference_form.html'
    success_url = reverse_lazy('intelligence:reference_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class AIReferenceDataDetailView(LoginRequiredMixin, DetailView):
    model = AIReferenceData
    template_name = 'intelligence/reference/reference_detail.html'
    context_object_name = 'reference'

class AIReferenceDataUpdateView(LoginRequiredMixin, UpdateView):
    model = AIReferenceData
    form_class = AIReferenceDataForm
    template_name = 'intelligence/reference/reference_form.html'
    success_url = reverse_lazy('intelligence:reference_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class AIReferenceDataDeleteView(LoginRequiredMixin, DeleteView):
    model = AIReferenceData
    template_name = 'intelligence/reference/reference_confirm_delete.html'
    success_url = reverse_lazy('intelligence:reference_list') 