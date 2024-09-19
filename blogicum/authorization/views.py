from django.shortcuts import redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm


class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('authorization:login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('blog:index')
