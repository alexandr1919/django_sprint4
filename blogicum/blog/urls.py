from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path(
        'posts/<int:post_id>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),
    path(
        'posts/<int:post_id>/edit',
        views.PostUpdateView.as_view(),
        name='edit_post'
    ),
    path(
        'posts/<int:post_id>/delete/',
        views.PostDeleteView.as_view(),
        name='delete_post',
    ),
    path(
        'profile/<str:username>/',
        views.ProfileListView.as_view(),
        name='profile'
    ),
    path(
        'category/<slug:category_slug>/',
        views.CategoryListView.as_view(),
        name='category_posts'
    ),
    path(
        'posts/<int:pk>/comment/',
        views.CommentCreateView.as_view(),
        name='add_comment',
    ),
    path(
        'posts/<int:pk>/edit_comment/<int:comment_pk>/',
        views.CommentUpdateView.as_view(),
        name='edit_comment',
    ),
    path(
        'profile/edit',
        views.ProfileUpdateView.as_view(),
        name='edit_profile',
    ),
    path(
        'posts/<int:pk>/delete_comment/<int:comment_pk>/',
        views.CommentDeleteView.as_view(),
        name='delete_comment',
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
