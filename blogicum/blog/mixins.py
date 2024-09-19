from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Post, Comment
from .forms import CreateCommentForm

User = get_user_model()


class PostMixin:
    model = Post
    pk_url_kwarg = 'post_id'


class CommentChangeMixin:
    model = Comment
    pk_url_kwarg = 'comment_pk'
    template_name = 'blog/comment.html'
    form_class = CreateCommentForm

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['pk']}
        )

    def get_object(self):
        object = get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
        return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.object
        return context


class AuthorAccessMixin(UserPassesTestMixin):
    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user
