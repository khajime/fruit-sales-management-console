import logging


from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


from . import models
from . import forms


logger = logging.getLogger(__name__)


class SaleListView(LoginRequiredMixin, ListView):
    """販売日時の降順で表示するリストビュー"""
    model = models.Sale
    template_name = 'fruitsales/fruitsale_list.html'
    login_url = 'login'

    def get_queryset(self):
        return self.model.objects.order_by('-sold_at')


class SaleCreateView(LoginRequiredMixin, CreateView):
    """販売情報登録ビュー
    * 入力された個数と果物マスタの単価から売り上げを計算して登録
    """
    model = models.Sale
    form_class = forms.SaleForm
    template_name = 'fruitsales/fruitsale_new.html'
    success_url = reverse_lazy('fruitsale_list')
    login_url = 'login'

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.object.fruit:
            # 果物の単価と個数から登録時点での売り上げを計算
            price = self.object.fruit.price
            self.object.amount = price * self.object.number
        else:
            # 指定がない場合は0
            self.object.amount = 0

        self.object.save()

        return response


# class SaleDetailView(DetailView):
#     model = models.Sale
#     template_name = 'fruitsales/fruitsale_detail.html'


class SaleUpdateView(LoginRequiredMixin, UpdateView):
    """販売情報編集ビュー"""
    model = models.Sale
    template_name = 'fruitsales/fruitsale_edit.html'
    fields = ['fruit', 'number', 'sold_at']
    login_url = 'login'


class SaleDeleteView(LoginRequiredMixin, DeleteView):
    """販売情報削除ビュー"""
    model = models.Sale
    template_name = 'fruitsales/fruitsale_delete.html'
    success_url = reverse_lazy('fruitsale_list')
    login_url = 'login'
    

@login_required
def sales_csv_input_view(request):
    """POSTされたCSVファイルを読み込みSaleレコードとしてDBに追加するビュー
    * 追加に成功した場合、追加されたレコードをリストで表示
    * 内容のバリデーションに失敗した場合、エラーページを表示
    """
    import csv
    if request.method == 'POST':
        logger.debug('received files: %s', list(request.FILES.items()))
        if 'records-csv' in request.FILES:
            try:
                sales = models.generate_sales_from_csv(request.FILES['records-csv'])
            except ValidationError as e:
                return  render(request, 'fruitsales/fruitsale_csv_input_failure.html', {'message': e.args[0]})
                        
            return render(request, 'fruitsales/fruitsale_csv_input_success.html', {'object_list': sales})
            
    return Http404()
