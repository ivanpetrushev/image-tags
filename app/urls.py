from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.tagstats),
    path('generate_sequence/<cat_ids>', views.generate_sequence),
    path('toggle/<file_id>/<tag_id>', views.toggle),
    path('set_is_tagged/<file_id>', views.set_is_tagged),
    path('get_needs_tagging', views.get_needs_tagging),
    path('set_needs_tagging/<file_id>', views.set_needs_tagging),
    path('get_cloud', views.get_cloud),
    path('get_counts', views.get_counts),
    path('get_file/<file_id>', views.get_file),
    path('new', views.new_tag),
    path('', views.tag),
]