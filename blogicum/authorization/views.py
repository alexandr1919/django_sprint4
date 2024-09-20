from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserCreateForm


class UserCreateView(CreateView):
    form_class = UserCreateForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('blog:index')
