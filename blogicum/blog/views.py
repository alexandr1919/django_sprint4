from django.db.models import Count
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from datetime import datetime
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.urls import reverse, reverse_lazy

from .models import Category, Post
from .mixins import PostMixin, AuthorAccessMixin, CommentChangeMixin
from .forms import CreatePostForm, EditUserForm, CreateCommentForm

User = get_user_model()
POST_PER_PAGE = 10


def get_posts(posts):
    return posts.filter(
        category__is_published=True
    ).select_related(
        'author', 'location', 'category'
    ).order_by('-pub_date').annotate(comment_count=Count('comments'))


class IndexListView(PostMixin, ListView):
    template_name = 'blog/index.html'
    paginate_by = POST_PER_PAGE

    def get_queryset(self):
        return get_posts(Post.objects).filter(
            is_published=True, pub_date__lte=datetime.today()
        )


class PostDetailView(PostMixin, DetailView):
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreateCommentForm()
        context['comments'] = (
            self.object.comments.prefetch_related('author').all()
        )
        return context


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
            kwargs={
                'username': self.request.user.username,
            })


class PostUpdateView(AuthorAccessMixin, PostMixin, UpdateView):
    form_class = CreatePostForm
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', post_id=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.object.pk}
        )


class PostDeleteView(AuthorAccessMixin, PostMixin, DeleteView):
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def get_object(self, queryset=None):
        return get_object_or_404(
            Post,
            pk=self.kwargs.get(self.pk_url_kwarg)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreatePostForm(instance=self.get_object())
        return context


class ProfileListView(PostMixin, ListView):
    template_name = 'blog/profile.html'
    paginate_by = POST_PER_PAGE

    def get_queryset(self):
        profile = get_object_or_404(User, username=self.kwargs['username'])
        posts = get_posts(Post.objects).filter(author=profile)
        if not self.request.user.id == profile.id:
            posts = posts.filter(
                is_published=True,
                pub_date__lte=timezone.now())
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(User, username=self.kwargs['username'])
        context['profile'] = profile
        return context


class ProfileUpdateView(UpdateView):
    model = User
    template_name = 'blog/user.html'
    form_class = EditUserForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={
                'username': self.request.user.username,
            },
        )

    def get_object(self):
        return self.request.user


class CategoryListView(PostMixin, ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = POST_PER_PAGE

    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return get_posts(self.category.posts.all()).filter(
            is_published=True,
            pub_date__lte=datetime.today()
        )

    def get_context_data(self, **kwargs):
        return dict(
            **super().get_context_data(**kwargs),
            category=self.category
        )


class CommentCreateView(CommentChangeMixin, LoginRequiredMixin, CreateView):
    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentDeleteView(CommentChangeMixin, AuthorAccessMixin, DeleteView):
    pass


class CommentUpdateView(CommentChangeMixin, AuthorAccessMixin, UpdateView):
    pass
