from django.contrib.auth import get_user_model
from django.db import models


CHAR_LEN = 256
TITLE_LEN = 20
User = get_user_model()


class BaseBlogModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )

    class Meta:
        ordering = ('created_at',)
        abstract = True


class Location(BaseBlogModel):
    name = models.CharField(
        max_length=256,
        verbose_name='Название места',
    )

    class Meta(BaseBlogModel.Meta):
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:TITLE_LEN]


class Category(BaseBlogModel):
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
    )
    description = models.TextField(verbose_name='Описание', null=False)
    slug = models.SlugField(
        unique=True,
        help_text='Идентификатор страницы для URL; '
                  'разрешены символы латиницы, цифры, дефис и подчёркивание.',
        verbose_name='Идентификатор',
    )

    class Meta(BaseBlogModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:TITLE_LEN]


class Post(BaseBlogModel):
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
    )
    text = models.TextField(max_length=256, verbose_name='Текст')
    pub_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время публикации',
        null=False,
        help_text='Если установить дату и время в будущем — '
                  'можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение',
        null=True,
        blank=True,
        related_name='posts'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True,
        related_name='posts'
    )
    image = models.ImageField('Изображение', blank=True, upload_to='img/')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title[:TITLE_LEN]


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             verbose_name='Публикация')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор')
    created_at = models.DateTimeField(
        verbose_name='Дата',
        auto_now_add=True,
    )

    class Meta:
        default_related_name = 'comments'
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:TITLE_LEN]
