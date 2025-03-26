"""
URL configuration for archivia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect, render

def redirect_to_login(request):
    return redirect('users:login')

urlpatterns = [
    path('', redirect_to_login, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),  # Toutes les URLs (pages web et API) avec le préfixe accounts/
    path('records/', include('records.urls')),  # URLs pour le module records (folders et documents)
    path('tools/', include('tools.urls')),  # URLs pour le module tools
    path('mails/', include('mails.urls')),  # URLs pour le module mail
    path('workspace/', include('workspace.urls')),  # URLs pour le module workspace
    path('intelligence/', include('intelligence.urls')),  # URLs pour le module intelligence
    path('projects/', include('projects.urls')),  # URLs pour le module projects
    path('tasks/', include('tasks.urls')),  # URLs pour le module tasks
    path('settings/', include('admin_panel.urls')),  # URLs pour le module settings
    path('correspondence/', include('correspondence.urls')),  # URLs pour le module correspondence
    path('examples/', lambda request: render(request, 'examples.html'), name='examples'),
]
