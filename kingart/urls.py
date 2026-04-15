from django.urls import path, include
from . import views 
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("", views.test, name = 'test'),
    path("blog/<int:id>/", views.read, name = 'read'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)