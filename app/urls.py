from django.urls import path
from . import views

urlpatterns = [
    path('bau', views.index, name='index'),
    path('stats/', views.tagstats, name='tagStats'),
    path('', views.tag, name='tag'),
]