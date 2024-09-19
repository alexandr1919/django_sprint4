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
from django.utils import timezone
from django.urls import reverse, reverse_lazy

from .models import Category, Post, User
from .mixins import PostMixin, AuthorAccessMixin, CommentChangeMixin
from .forms import CreateCommentForm, CreatePostForm, EditUserForm

POSTS_PER_PAGE = 10


def get_posts(
    posts=Post.objects,
    filter_by_is_published=True,
    count_comments=True,
):
    posts = posts.select_related(
        'author', 'location', 'category'
    )
    if filter_by_is_published:
        posts = posts.filter(is_published=True, category__is_published=True)
    if count_comments:
        posts = posts.annotate(comment_count=Count('comments'))
    return posts.order_by('-pub_date')


def get_author(user):
    return get_object_or_404(User, username=user.kwargs['username'])


class IndexListView(PostMixin, ListView):
    template_name = 'blog/index.html'
    paginate_by = POSTS_PER_PAGE
    queryset = get_posts(Post.objects).filter(pub_date__lte=datetime.today())


class PostDetailView(PostMixin, DetailView):
    template_name = 'blog/detail.html'

    def get_object(self):
        post = get_object_or_404(
            Post.objects,
            id=self.kwargs.get(self.pk_url_kwarg)
        )
        is_author = self.request.user == post.author
        if is_author:
            return post

        return get_object_or_404(
            get_posts(Post.objects, not is_author, not is_author),
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
                            post_id=self.kwargs.get('post_id'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs.get('post_id')}
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

    def get_queryset(self):
        author = get_author(self)
        is_author = self.request.user == author
        posts = get_posts(author.posts.all(), not is_author)
        if not is_author:
            posts = posts.filter(pub_date__lte=timezone.now())
        return posts

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            **kwargs,
            profile=get_author(self),
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

    def get_queryset(self):
        category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return get_posts(category.posts.all()).filter(
            pub_date__lte=datetime.today()
        )

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            **kwargs,
            category=get_object_or_404(
                Category,
                slug=self.kwargs['category_slug'],
                is_published=True
            ),
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
