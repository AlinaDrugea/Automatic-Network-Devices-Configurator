from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name = 'index.html'),name = 'login'),
    path('dashboard/',views.show_projects, name = 'project'),
    path('project/<str:project_id>/', views.show_projects_devices, name= 'projects'),
    path('save_config/',views.save_interface_config,name = 'save_config')
]