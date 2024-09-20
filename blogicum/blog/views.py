from datetime import datetime

from django.db.models import Count
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from .models import Category, Post, User
from .mixins import PostMixin, AuthorAccessMixin, CommentChangeMixin
from .forms import CreateCommentForm, CreatePostForm, EditUserForm

POSTS_PER_PAGE = 10


def get_posts(
    posts=Post.objects,
    *,
    filter_by_is_published=True,
    count_comments=True,
    join_related=True,
):
    if join_related:
        posts = posts.select_related('author', 'location', 'category')
    if filter_by_is_published:
        posts = posts.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=datetime.today()
        )
    if count_comments:
        return posts.annotate(comment_count=Count('comments')).order_by(
            '-pub_date'
        )
    return posts


class IndexListView(PostMixin, ListView):
    template_name = 'blog/index.html'
    paginate_by = POSTS_PER_PAGE
    queryset = get_posts(Post.objects)


class PostDetailView(PostMixin, DetailView):
    template_name = 'blog/detail.html'

    def get_object(self):
        post = get_object_or_404(
            Post.objects,
            id=self.kwargs.get(self.pk_url_kwarg)
        )
        if self.request.user == post.author:
            return post
        return get_object_or_404(
            get_posts(
                Post.objects,
                count_comments=False,
                join_related=False
            ),
            id=self.kwargs.get(self.pk_url_kwarg)
        )

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            **kwargs,
            form=CreateCommentForm(),
            comments=self.object.comments.prefetch_related('author').all()
        )


class PostCreateView(LoginRequiredMixin, PostMixin, CreateView):
    form_class = CreatePostForm
    template_name = 'blog/create.html'
    queryset = Post.objects.select_related('author', 'location', 'category')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            args=[self.request.user.username]
        )


class PostUpdateView(AuthorAccessMixin, PostMixin, UpdateView):
    form_class = CreatePostForm
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail',
                            post_id=self.kwargs.get(self.pk_url_kwarg))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', args=[self.kwargs.get(self.pk_url_kwarg)]
        )


class PostDeleteView(AuthorAccessMixin, PostMixin, DeleteView):
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            **kwargs,
            form=CreatePostForm(instance=self.get_object()),
        )


class ProfileListView(PostMixin, ListView):
    template_name = 'blog/profile.html'
    paginate_by = POSTS_PER_PAGE

    def get_author(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_queryset(self):
        author = self.get_author()
        return get_posts(
            author.posts.all(),
            filter_by_is_published=self.request.user != author
        )

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            **kwargs,
            profile=self.get_author(),
        )


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    form_class = EditUserForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            args=[self.request.user.username]
        )

    def get_object(self):
        return self.request.user


class CategoryListView(PostMixin, ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = POSTS_PER_PAGE

    def get_category(self):
        return get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )

    def get_queryset(self):
        return get_posts(self.get_category().posts.all())

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            **kwargs,
            category=self.get_category()
        )


class CommentCreateView(CommentChangeMixin, LoginRequiredMixin, CreateView):
    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentDeleteView(CommentChangeMixin, AuthorAccessMixin, DeleteView):
    pass


class CommentUpdateView(CommentChangeMixin, AuthorAccessMixin, UpdateView):
    pass
