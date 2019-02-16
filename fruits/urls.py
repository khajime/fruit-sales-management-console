from django.urls import path


from . import views


urlpatterns = [
    path('', views.FruitListView.as_view(), name='fruit_list'),
    path('new/', views.FruitCreateView.as_view(), name='fruit_new'),
    path('edit/<int:pk>/', views.FruitEditView.as_view(), name='fruit_edit'),
    path('delete/<int:pk>/', views.FruitDeleteView.as_view(), name='fruit_delete'),
]