from django.urls import path
from . import views

app_name = 'users'

# Pages web
urlpatterns = [
    path('', views.login_view, name='login'),  # Page par défaut
    path('register/', views.register, name='register'),
    path('welcome/', views.welcome, name='welcome'),
    path('logout/', views.logout_view, name='logout'),
]

# API endpoints
urlpatterns += [
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('groups/', views.group_views, name='group_list'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('groups/<int:group_id>/add_user/', views.add_user_to_group, name='add_user_to_group'),
] 