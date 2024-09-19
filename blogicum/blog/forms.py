from django.forms import DateTimeInput, ModelForm

from .models import Post, User, Comment


class EditUserForm(ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")


class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('author',)
        widgets = {
            'pub_date': DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                },
                format='%Y-%m-%dT%H:%M',
            ),
        }


class CreateCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
