from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


from . import models


class FruitListView(LoginRequiredMixin, ListView):
    """果物マスタリストビュー"""
    model = models.Fruit
    login_url = 'login'

    def get_queryset(self):
        return self.model.objects.order_by('-updated_at')


class FruitCreateView(LoginRequiredMixin, CreateView):
    """果物マスタ登録ビュー"""
    model = models.Fruit
    template_name = 'fruits/fruit_new.html'
    fields = ('name', 'price')
    login_url = 'login'


# class FruitDetailView(DetailView):
#     model = models.Fruit
#     template_name = 'fruits/fruit_list.html'
#     fields = '__all__'


class FruitEditView(LoginRequiredMixin, UpdateView):
    """果物マスタ編集ビュー"""
    model = models.Fruit
    template_name = 'fruits/fruit_edit.html'
    fields = ('name', 'price')
    login_url = 'login'


class FruitDeleteView(LoginRequiredMixin, DeleteView):
    """果物マスタ削除ビュー"""
    model = models.Fruit
    success_url = reverse_lazy('fruit_list')
    login_url = 'login'