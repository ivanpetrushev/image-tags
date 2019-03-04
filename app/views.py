from django.shortcuts import render
from django.http import HttpResponse
from .models import Tag, File, FileTag
from django.db.models import Count
from django.template import loader
from random import randint, shuffle

# Create your views here.


def tag(request):
    return HttpResponse('tag index')


def tagstats(request):
    tags = Tag.objects.annotate(num_tags=Count('filetag')).order_by('-num_tags')
    context = {
        'tags': tags
    }
    return render(request, 'app/index.html', context)


def generate_sequence(request, cat_ids='rand'):
    if cat_ids == 'rand':
        count = Tag.objects.count()
        rand_tag_id = Tag.objects.all()[randint(0, count - 1)].id
        tag_ids = [rand_tag_id]
    else:
        tag_ids = cat_ids.split(',')

    data = FileTag.objects.filter(tag_id__in=tag_ids)
    data = list(data)
    print(data)
    shuffle(data)
    print(data)
    return HttpResponse(' ei go ', tag_ids)


def toggle(request, file_id, tag_id):
    found = FileTag.objects.filter(tag_id=tag_id, file_id=file_id).count()
    if found:
        FileTag.objects.filter(tag_id=tag_id, file_id=file_id).delete()
    else:
        FileTag(tag_id=tag_id, file_id=file_id).save()
    return HttpResponse('success')


def set_tagged(request, file_id):
    file = File.objects.filter(id=file_id)
    if file:
        file.needs_tagging = 0
        file.save()
    return HttpResponse('success')


def set_not_tagged(request, file_id):
    file = File.objects.filter(id=file_id)
    if file:
        file.needs_tagging = 1
        file.save()
    return HttpResponse('success')


def get_needs_tagging(request):
    files = File.objects.filter(needs_tagging=1)
    files = shuffle(list(files))
    return HttpResponse('success')
