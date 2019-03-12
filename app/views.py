import mimetypes
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Tag, File, FileTag
from django.db.models import Count
from django.template import loader
from random import randint, shuffle
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def tag(request):
    return render(request, 'app/tag.html')
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

    data = FileTag.objects.filter(tag_id__in=tag_ids).values_list('file__id', flat=True)
    data = list(data)
    shuffle(data)
    context = {
        'data': data
    }
    return render(request, 'app/play.html', context)


def toggle(request, file_id, tag_id):
    found = FileTag.objects.filter(tag_id=tag_id, file_id=file_id).count()
    if found:
        FileTag.objects.filter(tag_id=tag_id, file_id=file_id).delete()
    else:
        FileTag(tag_id=tag_id, file_id=file_id).save()
    return JsonResponse({'success': True})


def get_file(request, file_id):
    file = File.objects.filter(id=file_id).first()
    if file:
        file.cnt_views += 1
        file.last_viewed = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.save()
        filepath = '/images/' + file.filename
        imagedata = open(filepath, 'rb').read()
        return HttpResponse(imagedata, content_type=mimetypes.guess_type(filepath))
    return JsonResponse({'success': False})


def set_is_tagged(request, file_id):
    file = File.objects.filter(id=file_id)
    if file:
        file.needs_tagging = 0
        file.save()
    return JsonResponse({'success': True})


def set_needs_tagging(request, file_id):
    file = File.objects.filter(id=file_id).first()
    if file:
        file.needs_tagging = 1
        file.save()
    return JsonResponse({'success': True})


def get_needs_tagging(request):
    data = File.objects.filter(needs_tagging=1).values()
    count = data.count()
    data = data[randint(0, count - 1)]
    return JsonResponse({'success': True, 'data': data})


def get_cloud(request):
    data = Tag.objects.order_by('name').values()
    data = list(data)
    return JsonResponse({'success': True, 'data': data})


@csrf_exempt
def new_tag(request):
    tag_name = request.POST['tag_name']
    Tag(name=tag_name).save()
    return JsonResponse({'success': True, 'tag_name': tag_name})
