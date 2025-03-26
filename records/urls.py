from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'records'

# URLs pour l'API REST
router = DefaultRouter()
router.register(r'folders', views.FolderViewSet, basename='folder')
router.register(r'documents', views.DocumentViewSet, basename='document')
router.register(r'metadata-definitions', views.MetadataDefinitionViewSet, basename='metadata-definition')
router.register(r'reference-lists', views.ReferenceListViewSet, basename='reference-list')
router.register(r'reference-values', views.ReferenceValueViewSet, basename='reference-value')

# URLs pour les vues templates
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
    
    # API URLs
    path('api/folders/<int:pk>/metadata/', views.FolderMetadataViewSet.as_view({'get': 'list', 'post': 'create'}), name='folder-metadata'),
    path('api/folders/<int:pk>/metadata/<int:metadata_id>/', views.FolderMetadataViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='folder-metadata-detail'),
    path('api/folders/<int:pk>/children/', views.FolderChildrenView.as_view(), name='folder-children'),
    path('api/folders/<int:pk>/tree/', views.FolderTreeView.as_view(), name='folder-tree'),
    path('api/', include(router.urls)),
] 