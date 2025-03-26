from django.urls import path
from . import views

app_name = 'records'

urlpatterns = [
    # Trash URL
    path('trash/', views.TrashView.as_view(), name='trash'),
    
    # Folder URLs
    path('folders/', views.FolderListView.as_view(), name='folder_list'),
    path('folders/create/', views.FolderCreateView.as_view(), name='folder_create'),
    path('folders/<int:pk>/', views.FolderDetailView.as_view(), name='folder_detail'),
    path('folders/<int:pk>/update/', views.FolderUpdateView.as_view(), name='folder_update'),
    path('folders/<int:pk>/delete/', views.FolderDeleteView.as_view(), name='folder_delete'),
    path('folders/<int:pk>/restore/', views.FolderRestoreView.as_view(), name='folder_restore'),
    
    # Document URLs
    path('documents/', views.DocumentListView.as_view(), name='document_list'),
    path('documents/import/', views.DocumentImportView.as_view(), name='document_import'),
    path('documents/create/', views.DocumentCreateView.as_view(), name='document_create'),
    path('documents/<int:pk>/', views.DocumentDetailView.as_view(), name='document_detail'),
    path('documents/<int:pk>/update/', views.DocumentUpdateView.as_view(), name='document_update'),
    path('documents/<int:pk>/delete/', views.DocumentDeleteView.as_view(), name='document_delete'),
    path('documents/<int:pk>/download/', views.DocumentDownloadView.as_view(), name='document_download'),
    path('documents/recent/', views.recent_documents, name='recent_documents'),
    path('documents/favorites/', views.favorite_documents, name='favorite_documents'),
    
    # Metadata URLs
    path('metadata-definitions/', views.MetadataDefinitionListView.as_view(), name='metadata_definition_list'),
    path('metadata-definitions/create/', views.MetadataDefinitionCreateView.as_view(), name='metadata_definition_create'),
    path('metadata-definitions/<int:pk>/', views.MetadataDefinitionDetailView.as_view(), name='metadata_definition_detail'),
    path('metadata-definitions/<int:pk>/update/', views.MetadataDefinitionUpdateView.as_view(), name='metadata_definition_update'),
    path('metadata-definitions/<int:pk>/delete/', views.MetadataDefinitionDeleteView.as_view(), name='metadata_definition_delete'),
    
    # Reference List URLs
    path('reference-lists/', views.ReferenceListListView.as_view(), name='reference_list_list'),
    path('reference-lists/create/', views.ReferenceListCreateView.as_view(), name='reference_list_create'),
    path('reference-lists/<int:pk>/', views.ReferenceListDetailView.as_view(), name='reference_list_detail'),
    path('reference-lists/<int:pk>/update/', views.ReferenceListUpdateView.as_view(), name='reference_list_update'),
    path('reference-lists/<int:pk>/delete/', views.ReferenceListDeleteView.as_view(), name='reference_list_delete'),
    
    # Reference Value URLs
    path('reference-values/create/<int:list_id>/', views.ReferenceValueCreateView.as_view(), name='reference_value_create'),
    path('reference-values/<int:pk>/update/', views.ReferenceValueUpdateView.as_view(), name='reference_value_update'),
    path('reference-values/<int:pk>/delete/', views.ReferenceValueDeleteView.as_view(), name='reference_value_delete'),
    
    # Category URLs
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/import/', views.CategoryImportView.as_view(), name='category_import'),
    path('categories/tree/', views.CategoryTreeView.as_view(), name='category_tree'),
    path('categories/stats/', views.CategoryStatsView.as_view(), name='category_stats'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    
    # Archive URLs
    path('archives/', views.ArchiveListView.as_view(), name='archive_list'),
    path('archives/create/', views.ArchiveCreateView.as_view(), name='archive_create'),
    path('archives/<int:pk>/', views.ArchiveDetailView.as_view(), name='archive_detail'),
    path('archives/<int:pk>/update/', views.ArchiveUpdateView.as_view(), name='archive_update'),
    path('archives/<int:pk>/delete/', views.ArchiveDeleteView.as_view(), name='archive_delete'),
    
    # Retention URLs
    path('retentions/', views.RetentionListView.as_view(), name='retention_list'),
    path('retentions/create/', views.RetentionCreateView.as_view(), name='retention_create'),
    path('retentions/<int:pk>/', views.RetentionDetailView.as_view(), name='retention_detail'),
    path('retentions/<int:pk>/update/', views.RetentionUpdateView.as_view(), name='retention_update'),
    path('retentions/<int:pk>/delete/', views.RetentionDeleteView.as_view(), name='retention_delete'),
    
    # Disposal URLs
    path('disposals/', views.DisposalListView.as_view(), name='disposal_list'),
    
    # Search URLs
    path('search/', views.SearchView.as_view(), name='search'),
    
    # Audit Log URLs
    path('audit-log/', views.AuditLogView.as_view(), name='audit_log'),
    
    # Export URLs
    path('export/', views.export_data, name='export'),
    
    # Settings URL
    path('settings/', views.settings, name='settings'),
] 