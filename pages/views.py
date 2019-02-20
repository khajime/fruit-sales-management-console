from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class TopPageView( LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    login_url = 'login'

