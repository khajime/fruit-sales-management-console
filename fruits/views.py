from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy


from . import models


class FruitListView(ListView):
    model = models.Fruit


class FruitCreateView(CreateView):
    model = models.Fruit
    template_name = 'fruits/fruit_new.html'
    fields = '__all__'

class FruitDetailView(DetailView):
    model = models.Fruit
    template_name = 'fruits/fruit_list.html'
    fields = '__all__'


class FruitEditView(UpdateView):
    model = models.Fruit
    template_name = 'fruits/fruit_edit.html'
    fields = '__all__'


class FruitDeleteView(DeleteView):
    model = models.Fruit
    success_url = reverse_lazy('fruit_list')