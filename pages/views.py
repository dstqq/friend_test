from urllib import request
from django.views.generic import TemplateView
from django.shortcuts import render


class HomePageView(TemplateView):
    template_name = 'homes/home.html'


class AboutPageView(TemplateView):
    template_name = 'homes/about.html'


def HelpPage(request):
    context = {}
    return render(request, 'homes/help.html', context=context)