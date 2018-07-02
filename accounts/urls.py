from django.urls import path, re_path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    re_path(r'^(?P<username>[\w-]+)/$', views.profile_view, name='profile'),
    re_path(r'^(?P<username>[\w-]+)/pp_upload/$', views.pp_upload_view, name='pp_upload'),
    re_path(r'^(?P<username>[\w-]+)/settings/$', views.settings_view, name='settings'),
]
