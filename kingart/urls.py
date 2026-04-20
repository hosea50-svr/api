from django.urls import path, include
from . import views 
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("", views.test, name = 'test'),
    path("blog/<int:id>/", views.read, name = 'read'),
    path("blog_api/", views.blog_list_api, name = 'blog_list_api'),
    path("post_blog_api/", views.post_blog_api, name = 'post_blog_api'),
    path("put_blog_api/", views.put_blog_api, name = 'put_blog_api'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)