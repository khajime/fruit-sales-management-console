from django.shortcuts import render
from django.views.generic import TemplateView


class TopPageView(TemplateView):
    template_name = 'home.html'

