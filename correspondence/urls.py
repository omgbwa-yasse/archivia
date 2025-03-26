from django.urls import path, include
from . import views

app_name = 'correspondence'

urlpatterns = [
    # Correspondence URLs
    path('', views.CorrespondenceListView.as_view(), name='list'),
    path('incoming/', views.IncomingCorrespondenceListView.as_view(), name='incoming'),
    path('outgoing/', views.OutgoingCorrespondenceListView.as_view(), name='outgoing'),
    path('internal/', views.InternalCorrespondenceListView.as_view(), name='internal'),
    path('recent/', views.RecentCorrespondenceListView.as_view(), name='recent'),
    path('favorites/', views.FavoritesCorrespondenceListView.as_view(), name='favorites'),
    path('create/', views.CorrespondenceCreateView.as_view(), name='create'),
    path('scan/', views.scan, name='scan'),
    path('<int:pk>/', views.CorrespondenceDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.CorrespondenceUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.CorrespondenceDeleteView.as_view(), name='delete'),
    path('<int:pk>/archive/', views.correspondence_archive, name='archive'),
    path('export/', views.export_data, name='export'),

    # Folder URLs
    path('folders/', views.FolderListView.as_view(), name='folder_list'),
    path('folders/create/', views.FolderCreateView.as_view(), name='folder_create'),
    path('folders/<int:pk>/', views.FolderDetailView.as_view(), name='folder_detail'),
    path('folders/<int:pk>/update/', views.FolderUpdateView.as_view(), name='folder_update'),
    path('folders/<int:pk>/delete/', views.FolderDeleteView.as_view(), name='folder_delete'),

    # Template URLs
    path('templates/', views.TemplateListView.as_view(), name='template_list'),
    path('templates/create/', views.TemplateCreateView.as_view(), name='template_create'),
    path('templates/<int:pk>/', views.TemplateDetailView.as_view(), name='template_detail'),
    path('templates/<int:pk>/update/', views.TemplateUpdateView.as_view(), name='template_update'),
    path('templates/<int:pk>/delete/', views.TemplateDeleteView.as_view(), name='template_delete'),

    # Batch URLs
    path('batches/', views.BatchListView.as_view(), name='batch_list'),
    path('batches/create/', views.BatchCreateView.as_view(), name='batch_create'),
    path('batches/<int:pk>/', views.BatchDetailView.as_view(), name='batch_detail'),
    path('batches/<int:pk>/update/', views.BatchUpdateView.as_view(), name='batch_update'),
    path('batches/<int:pk>/delete/', views.BatchDeleteView.as_view(), name='batch_delete'),
    
    # Batch Correspondence URLs
    path('batches/<int:batch_pk>/add-correspondence/<int:correspondence_pk>/', 
         views.add_correspondence_to_batch, name='add_to_batch'),
    path('batches/<int:batch_pk>/remove-correspondence/<int:correspondence_pk>/', 
         views.remove_correspondence_from_batch, name='remove_from_batch'),
]