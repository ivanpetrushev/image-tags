from django.shortcuts import render
from django.http import HttpResponse
from .models import Tag, File, FileTag
from django.db.models import Count
from django.template import loader

# Create your views here.


def index(request):
    return HttpResponse('Bau!')


def tag(request):
    return HttpResponse('tag index')


def tagstats(request):
    tags = Tag.objects.annotate(num_tags=Count('filetag')).order_by('-num_tags')
    context = {
        'tags': tags
    }
    return render(request, 'app/index.html', context)
