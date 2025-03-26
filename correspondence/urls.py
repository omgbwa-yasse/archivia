from django.urls import path, include
from . import views

app_name = 'correspondence'

urlpatterns = [
    # Correspondence URLs
    path('', views.CorrespondenceListView.as_view(), name='list'),
    path('create/', views.CorrespondenceCreateView.as_view(), name='create'),
    path('<int:pk>/', views.CorrespondenceDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.CorrespondenceUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.CorrespondenceDeleteView.as_view(), name='delete'),
    path('<int:pk>/archive/', views.correspondence_archive, name='archive'),

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

urlpatterns += [
    path('correspondence/', include('correspondence.urls')),
] 