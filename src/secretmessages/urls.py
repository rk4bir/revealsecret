from django.urls import path, re_path
from . import views
app_name = 'messages'

urlpatterns = [
	path('<int:pk>/favourite/', views.favourite_view, name='favourite'),
	path('<int:pk>/delete/', views.delete_view, name='delete'),
]