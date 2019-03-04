from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.tagstats),
    path('generate_sequence/<cat_ids>', views.generate_sequence),
    path('toggle/<file_id>/<tag_id>', views.toggle),
    path('set_tagged/<file_id>', views.set_tagged),
    path('set_not_tagged/<file_id>', views.set_not_tagged),
    path('get_needs_tagging', views.get_needs_tagging),
    path('', views.tag),
]