from django.urls import path
from . import views

app_name = 'tools'

urlpatterns = [
    # Communicability URLs
    path('communicability/', views.CommunicabilityListView.as_view(), name='communicability_list'),
    path('communicability/create/', views.CommunicabilityCreateView.as_view(), name='communicability_create'),
    path('communicability/<int:pk>/', views.CommunicabilityDetailView.as_view(), name='communicability_detail'),
    path('communicability/<int:pk>/update/', views.CommunicabilityUpdateView.as_view(), name='communicability_update'),
    path('communicability/<int:pk>/delete/', views.CommunicabilityDeleteView.as_view(), name='communicability_delete'),

    # Activity URLs
    path('activity/', views.ActivityListView.as_view(), name='activity_list'),
    path('activity/create/', views.ActivityCreateView.as_view(), name='activity_create'),
    path('activity/<int:pk>/', views.ActivityDetailView.as_view(), name='activity_detail'),
    path('activity/<int:pk>/update/', views.ActivityUpdateView.as_view(), name='activity_update'),
    path('activity/<int:pk>/delete/', views.ActivityDeleteView.as_view(), name='activity_delete'),

    # Sort URLs
    path('sort/', views.SortListView.as_view(), name='sort_list'),
    path('sort/create/', views.SortCreateView.as_view(), name='sort_create'),
    path('sort/<int:pk>/', views.SortDetailView.as_view(), name='sort_detail'),
    path('sort/<int:pk>/update/', views.SortUpdateView.as_view(), name='sort_update'),
    path('sort/<int:pk>/delete/', views.SortDeleteView.as_view(), name='sort_delete'),

    # Retention URLs
    path('retention/', views.RetentionListView.as_view(), name='retention_list'),
    path('retention/create/', views.RetentionCreateView.as_view(), name='retention_create'),
    path('retention/<int:pk>/', views.RetentionDetailView.as_view(), name='retention_detail'),
    path('retention/<int:pk>/update/', views.RetentionUpdateView.as_view(), name='retention_update'),
    path('retention/<int:pk>/delete/', views.RetentionDeleteView.as_view(), name='retention_delete'),

    # LawType URLs
    path('law-type/', views.LawTypeListView.as_view(), name='law_type_list'),
    path('law-type/create/', views.LawTypeCreateView.as_view(), name='law_type_create'),
    path('law-type/<int:pk>/', views.LawTypeDetailView.as_view(), name='law_type_detail'),
    path('law-type/<int:pk>/update/', views.LawTypeUpdateView.as_view(), name='law_type_update'),
    path('law-type/<int:pk>/delete/', views.LawTypeDeleteView.as_view(), name='law_type_delete'),

    # Law URLs
    path('law/', views.LawListView.as_view(), name='law_list'),
    path('law/create/', views.LawCreateView.as_view(), name='law_create'),
    path('law/<int:pk>/', views.LawDetailView.as_view(), name='law_detail'),
    path('law/<int:pk>/update/', views.LawUpdateView.as_view(), name='law_update'),
    path('law/<int:pk>/delete/', views.LawDeleteView.as_view(), name='law_delete'),

    # LawArticle URLs
    path('law-article/', views.LawArticleListView.as_view(), name='law_article_list'),
    path('law-article/create/', views.LawArticleCreateView.as_view(), name='law_article_create'),
    path('law-article/<int:pk>/', views.LawArticleDetailView.as_view(), name='law_article_detail'),
    path('law-article/<int:pk>/update/', views.LawArticleUpdateView.as_view(), name='law_article_update'),
    path('law-article/<int:pk>/delete/', views.LawArticleDeleteView.as_view(), name='law_article_delete'),

    # RetentionLawArticle URLs
    path('retention-law-article/', views.RetentionLawArticleListView.as_view(), name='retention_law_article_list'),
    path('retention-law-article/create/', views.RetentionLawArticleCreateView.as_view(), name='retention_law_article_create'),
    path('retention-law-article/<int:pk>/', views.RetentionLawArticleDetailView.as_view(), name='retention_law_article_detail'),
    path('retention-law-article/<int:pk>/update/', views.RetentionLawArticleUpdateView.as_view(), name='retention_law_article_update'),
    path('retention-law-article/<int:pk>/delete/', views.RetentionLawArticleDeleteView.as_view(), name='retention_law_article_delete'),

    # Organisation URLs
    path('organisation/', views.OrganisationListView.as_view(), name='organisation_list'),
    path('organisation/create/', views.OrganisationCreateView.as_view(), name='organisation_create'),
    path('organisation/<int:pk>/', views.OrganisationDetailView.as_view(), name='organisation_detail'),
    path('organisation/<int:pk>/update/', views.OrganisationUpdateView.as_view(), name='organisation_update'),
    path('organisation/<int:pk>/delete/', views.OrganisationDeleteView.as_view(), name='organisation_delete'),

    # OrganisationActivity URLs
    path('organisation-activity/', views.OrganisationActivityListView.as_view(), name='organisation_activity_list'),
    path('organisation-activity/create/', views.OrganisationActivityCreateView.as_view(), name='organisation_activity_create'),
    path('organisation-activity/<int:pk>/', views.OrganisationActivityDetailView.as_view(), name='organisation_activity_detail'),
    path('organisation-activity/<int:pk>/update/', views.OrganisationActivityUpdateView.as_view(), name='organisation_activity_update'),
    path('organisation-activity/<int:pk>/delete/', views.OrganisationActivityDeleteView.as_view(), name='organisation_activity_delete'),
] 