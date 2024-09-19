from django.contrib.auth import get_user_model
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
            args=[self.kwargs['post_id']]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.object
        return context


class AuthorAccessMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author == self.request.user
