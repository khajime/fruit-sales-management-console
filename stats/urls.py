from django.urls import path


from . import views


urlpatterns = [
    path('', views.fruitsale_stats_view, name='fruitsale_stats'),
]