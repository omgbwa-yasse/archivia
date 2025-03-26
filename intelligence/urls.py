from django.urls import path
from . import views

app_name = 'intelligence'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('analysis/', views.analysis, name='analysis'),
    path('predictions/', views.predictions, name='predictions'),
    path('training/', views.training, name='training'),
    path('evaluation/', views.evaluation, name='evaluation'),
    # AI Agents URLs
    path('agents/', views.AIAgentListView.as_view(), name='agent_list'),
    path('agents/create/', views.AIAgentCreateView.as_view(), name='agent_create'),
    path('agents/<int:pk>/', views.AIAgentDetailView.as_view(), name='agent_detail'),
    path('agents/<int:pk>/update/', views.AIAgentUpdateView.as_view(), name='agent_update'),
    path('agents/<int:pk>/delete/', views.AIAgentDeleteView.as_view(), name='agent_delete'),
    
    # AI Models URLs
    path('models/', views.AIModelListView.as_view(), name='model_list'),
    path('models/create/', views.AIModelCreateView.as_view(), name='model_create'),
    path('models/<int:pk>/', views.AIModelDetailView.as_view(), name='model_detail'),
    path('models/<int:pk>/update/', views.AIModelUpdateView.as_view(), name='model_update'),
    path('models/<int:pk>/delete/', views.AIModelDeleteView.as_view(), name='model_delete'),
    
    # AI Prompts URLs
    path('prompts/', views.AIPromptListView.as_view(), name='prompt_list'),
    path('prompts/create/', views.AIPromptCreateView.as_view(), name='prompt_create'),
    path('prompts/<int:pk>/', views.AIPromptDetailView.as_view(), name='prompt_detail'),
    path('prompts/<int:pk>/update/', views.AIPromptUpdateView.as_view(), name='prompt_update'),
    path('prompts/<int:pk>/delete/', views.AIPromptDeleteView.as_view(), name='prompt_delete'),
    path('prompts/<int:pk>/versions/', views.AIPromptVersionListView.as_view(), name='prompt_versions'),
    
    # AI Chats URLs
    path('chats/', views.AIChatListView.as_view(), name='chat_list'),
    path('chats/create/', views.AIChatCreateView.as_view(), name='chat_create'),
    path('chats/<int:pk>/', views.AIChatDetailView.as_view(), name='chat_detail'),
    path('chats/<int:pk>/update/', views.AIChatUpdateView.as_view(), name='chat_update'),
    path('chats/<int:pk>/delete/', views.AIChatDeleteView.as_view(), name='chat_delete'),
    path('chats/<int:pk>/archive/', views.chat_archive, name='chat_archive'),
    path('chats/<int:pk>/messages/', views.AIChatMessageListView.as_view(), name='chat_messages'),
    path('chats/<int:pk>/messages/create/', views.AIChatMessageCreateView.as_view(), name='chat_message_create'),
    
    # AI Tools URLs
    path('tools/', views.AIToolListView.as_view(), name='tool_list'),
    path('tools/create/', views.AIToolCreateView.as_view(), name='tool_create'),
    path('tools/<int:pk>/', views.AIToolDetailView.as_view(), name='tool_detail'),
    path('tools/<int:pk>/update/', views.AIToolUpdateView.as_view(), name='tool_update'),
    path('tools/<int:pk>/delete/', views.AIToolDeleteView.as_view(), name='tool_delete'),
    
    # AI Tasks URLs
    path('tasks/', views.AITaskListView.as_view(), name='task_list'),
    path('tasks/create/', views.AITaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/', views.AITaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:pk>/update/', views.AITaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', views.AITaskDeleteView.as_view(), name='task_delete'),
    path('tasks/<int:pk>/start/', views.task_start, name='task_start'),
    path('tasks/<int:pk>/complete/', views.task_complete, name='task_complete'),
    path('tasks/<int:pk>/fail/', views.task_fail, name='task_fail'),
    path('tasks/<int:pk>/cancel/', views.task_cancel, name='task_cancel'),
    path('tasks/<int:pk>/feedback/', views.AITaskFeedbackCreateView.as_view(), name='task_feedback'),
    
    # AI Usage Stats URLs
    path('stats/', views.AIUsageStatListView.as_view(), name='usage_stats'),
    path('stats/export/', views.usage_stats_export, name='usage_stats_export'),
    
    # AI Reference Data URLs
    path('references/', views.AIReferenceDataListView.as_view(), name='reference_list'),
    path('references/create/', views.AIReferenceDataCreateView.as_view(), name='reference_create'),
    path('references/<int:pk>/', views.AIReferenceDataDetailView.as_view(), name='reference_detail'),
    path('references/<int:pk>/update/', views.AIReferenceDataUpdateView.as_view(), name='reference_update'),
    path('references/<int:pk>/delete/', views.AIReferenceDataDeleteView.as_view(), name='reference_delete'),
] 