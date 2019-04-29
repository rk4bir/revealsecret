from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from main import views

urlpatterns = [
	path('', views.index_view, name='homepage'),
	path('about/', views.about_view, name='about'),
	path('admin/', admin.site.urls),
	path('accounts/', include('accounts.urls')),
	path('messages/', include('secretmessages.urls')),
	path('not-authorized/', views.not_authorized_view, name='not-authorized'),
    re_path(r'^(?P<username>[\w-]+)/$', views.send_message_view, name='message'),    
]


if settings.DEBUG:
    #urlpatterns += (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
    urlpatterns += (static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
