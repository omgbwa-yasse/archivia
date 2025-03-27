from django.urls import path
from . import views

app_name = 'correspondence'

urlpatterns = [
    # Correspondence views
    path('', views.CorrespondenceListView.as_view(), name='list'),
    path('incoming/', views.IncomingCorrespondenceListView.as_view(), name='incoming_list'),
    path('outgoing/', views.OutgoingCorrespondenceListView.as_view(), name='outgoing_list'),
    path('internal/', views.InternalCorrespondenceListView.as_view(), name='internal_list'),
    path('recent/', views.RecentCorrespondenceListView.as_view(), name='recent_list'),
    path('favorites/', views.FavoritesCorrespondenceListView.as_view(), name='favorites_list'),
    path('create/', views.CorrespondenceCreateView.as_view(), name='create'),
    path('<int:pk>/', views.CorrespondenceDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.CorrespondenceUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.CorrespondenceDeleteView.as_view(), name='delete'),

    # Folder views
    path('folders/', views.CorrespondenceFolderListView.as_view(), name='folder_list'),
    path('folders/create/', views.CorrespondenceFolderCreateView.as_view(), name='folder_create'),
    path('folders/<int:pk>/', views.CorrespondenceFolderDetailView.as_view(), name='folder_detail'),
    path('folders/<int:pk>/update/', views.CorrespondenceFolderUpdateView.as_view(), name='folder_update'),
    path('folders/<int:pk>/delete/', views.CorrespondenceFolderDeleteView.as_view(), name='folder_delete'),

    # Template views
    path('templates/', views.CorrespondenceTemplateListView.as_view(), name='template_list'),
    path('templates/create/', views.CorrespondenceTemplateCreateView.as_view(), name='template_create'),
    path('templates/<int:pk>/', views.CorrespondenceTemplateDetailView.as_view(), name='template_detail'),
    path('templates/<int:pk>/update/', views.CorrespondenceTemplateUpdateView.as_view(), name='template_update'),
    path('templates/<int:pk>/delete/', views.CorrespondenceTemplateDeleteView.as_view(), name='template_delete'),

    # Batch views
    path('batches/', views.CorrespondenceBatchListView.as_view(), name='batch_list'),
    path('batches/create/', views.CorrespondenceBatchCreateView.as_view(), name='batch_create'),
    path('batches/<int:pk>/', views.CorrespondenceBatchDetailView.as_view(), name='batch_detail'),
    path('batches/<int:pk>/update/', views.CorrespondenceBatchUpdateView.as_view(), name='batch_update'),
    path('batches/<int:pk>/delete/', views.CorrespondenceBatchDeleteView.as_view(), name='batch_delete'),

    # Attachment views
    path('attachments/', views.CorrespondenceAttachmentListView.as_view(), name='attachment_list'),
    path('attachments/create/', views.CorrespondenceAttachmentCreateView.as_view(), name='attachment_create'),
    path('attachments/<int:pk>/', views.CorrespondenceAttachmentDetailView.as_view(), name='attachment_detail'),
    path('attachments/<int:pk>/update/', views.CorrespondenceAttachmentUpdateView.as_view(), name='attachment_update'),
    path('attachments/<int:pk>/delete/', views.CorrespondenceAttachmentDeleteView.as_view(), name='attachment_delete'),

    # Related correspondence views
    path('related/', views.CorrespondenceRelatedListView.as_view(), name='related_list'),
    path('related/create/', views.CorrespondenceRelatedCreateView.as_view(), name='related_create'),
    path('related/<int:pk>/', views.CorrespondenceRelatedDetailView.as_view(), name='related_detail'),
    path('related/<int:pk>/update/', views.CorrespondenceRelatedUpdateView.as_view(), name='related_update'),
    path('related/<int:pk>/delete/', views.CorrespondenceRelatedDeleteView.as_view(), name='related_delete'),

    # Priority views
    path('priorities/', views.CorrespondencePriorityListView.as_view(), name='priority_list'),
    path('priorities/create/', views.CorrespondencePriorityCreateView.as_view(), name='priority_create'),
    path('priorities/<int:pk>/', views.CorrespondencePriorityDetailView.as_view(), name='priority_detail'),
    path('priorities/<int:pk>/update/', views.CorrespondencePriorityUpdateView.as_view(), name='priority_update'),
    path('priorities/<int:pk>/delete/', views.CorrespondencePriorityDeleteView.as_view(), name='priority_delete'),

    # Typology views
    path('typologies/', views.CorrespondenceTypologyListView.as_view(), name='typology_list'),
    path('typologies/create/', views.CorrespondenceTypologyCreateView.as_view(), name='typology_create'),
    path('typologies/<int:pk>/', views.CorrespondenceTypologyDetailView.as_view(), name='typology_detail'),
    path('typologies/<int:pk>/update/', views.CorrespondenceTypologyUpdateView.as_view(), name='typology_update'),
    path('typologies/<int:pk>/delete/', views.CorrespondenceTypologyDeleteView.as_view(), name='typology_delete'),

    # Action views
    path('actions/', views.CorrespondenceActionListView.as_view(), name='action_list'),
    path('actions/create/', views.CorrespondenceActionCreateView.as_view(), name='action_create'),
    path('actions/<int:pk>/', views.CorrespondenceActionDetailView.as_view(), name='action_detail'),
    path('actions/<int:pk>/update/', views.CorrespondenceActionUpdateView.as_view(), name='action_update'),
    path('actions/<int:pk>/delete/', views.CorrespondenceActionDeleteView.as_view(), name='action_delete'),
]