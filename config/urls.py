from django.urls import path, include

urlpatterns = [
    # ... other patterns ...
    path('correspondence/', include('correspondence.urls')),
] 