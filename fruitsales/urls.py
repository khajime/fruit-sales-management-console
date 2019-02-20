from django.urls import path


from . import views


urlpatterns = [
    path('', views.SaleListView.as_view(), name='fruitsale_list'),
    path('new/', views.SaleCreateView.as_view(), name='fruitsale_new'),
    path('<int:pk>/edit/', views.SaleUpdateView.as_view(), name='fruitsale_edit'),
    path('<int:pk>/delete/', views.SaleDeleteView.as_view(), name='fruitsale_delete'),
    path('csv_input/', views.sales_csv_input_view, name='fruitsale_csv_input'),
]