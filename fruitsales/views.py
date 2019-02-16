from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy


from . import models


class SaleListView(ListView):
    model = models.Sale
    template_name = 'fruitsales/fruitsale_list.html'


class SaleCreateView(CreateView):
    model = models.Sale
    template_name = 'fruitsales/fruitsale_new.html'
    fields = ['fruit', 'number', 'sold_at']


class SaleDetailView(DetailView):
    model = models.Sale
    template_name = 'fruitsales/fruitsale_detail.html'


class SaleUpdateView(UpdateView):
    model = models.Sale
    template_name = 'fruitsales/fruitsale_edit.html'
    fields = ['fruit', 'number', 'sold_at']


class SaleDeleteView(DeleteView):
    model = models.Sale
    success_url = reverse_lazy('fruitsale_list')
