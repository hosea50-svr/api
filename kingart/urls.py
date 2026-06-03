from django.urls import path, include
from . import views 
from django.conf import settings
from django.conf.urls.static import static
from .views import contact_view


urlpatterns = [
    path("", views.test, name = 'test'),
    path("post/", views.post, name = 'post'),
    path("blog/<int:id>/", views.read, name = 'read'),
    path("blog/update/<int:id>/", views.update, name = 'update'),
    path("blog/delete/<int:id>/", views.blog_delete, name="blog_delete"),
    path("login/",views.login, name="login"),

    #Class base API
    path('api/register/', views.RegisterView.as_view(), name="register"),
    path('api/login/', views.LoginView.as_view(), name='login'),
    path('class/blogs/', views.BlogListCreateAPIView.as_view(), name="api-blog"),
    path('class/blogs/<int:id>/', views.BlogDetailAPIView.as_view(), name="api-blog-id"),

    path("api/contact/", contact_view),

    #Comment api
     path(
        "posts/<int:blog_id>/comments/",
        views.CommentListCreateView.as_view(),
        name="comments"
    ),
    #email
    path("contact/", views.contact, name="contact"),

    #like section
    path('posts/<int:post_id>/like/', views.LikePostView.as_view()),

    #API Urls (Functional views)
    # path('api/blog/', views.blog_list_create_api),
    # path('api/blog/<int:id>/', views.blog_detail_api),

    #Single API set-up
    # path("api/blog/get/", views.blog_get_api, name = 'api_get'),
    # path("api/blog/post/", views.blog_post_api, name = 'api_post'),
    # path("api/blog/put/", views.blog_put_api, name = 'api_put'),
    # path("api/blog/delete/<int:id>/", views.blog_delete_api, name="api_delete"), 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)