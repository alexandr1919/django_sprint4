from django.shortcuts import render
from django.views.generic import TemplateView

from .constants import HTTPStatusCodes


class AboutTemplateView(TemplateView):
    template_name = 'pages/about.html'


class RulesTemplateView(TemplateView):
    template_name = 'pages/rules.html'


def handler403(request, exception):
    return render(
        request,
        'pages/403.html',
        status=HTTPStatusCodes.NOT_ALLOWED,
    )


def csrf_failure(request, reason=''):
    return render(
        request,
        'pages/403csrf.html',
        status=HTTPStatusCodes.NOT_ALLOWED,
    )


def handler404(request, exception):
    return render(
        request,
        'pages/404.html',
        status=HTTPStatusCodes.NOT_FOUND,
    )


def handler500(request):
    return render(
        request,
        'pages/500.html',
        status=HTTPStatusCodes.SERVER_ERROR,
    )
