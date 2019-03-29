import mimetypes
import pickle
import numpy
from itertools import combinations
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Tag, File, FileTag
from django.db.models import Count
from django.template import loader
from random import randint, shuffle
from django.views.decorators.csrf import csrf_exempt
from collections import defaultdict
from django.core.cache import cache


def tag(request):
    return render(request, 'app/tag.html')
    return HttpResponse('tag index')


def tagstats(request):
    # get generic tag -> count stats
    tags = Tag.objects.annotate(num_tags=Count('filetag')).order_by('-num_tags')
    tag_chunks = numpy.array_split(tags, 5)
    tag_chunks = numpy.array(tag_chunks).transpose()

    # get doublets and triplets
    (doublets, triplets) = generate_doublets_triplets()
    doublets_chunks = numpy.array_split(doublets, 5)
    doublets_chunks = numpy.array(doublets_chunks).transpose()
    triplets_chunks = numpy.array_split(triplets, 3)
    triplets_chunks = numpy.array(triplets_chunks).transpose()

    context = {
        'tags': tags,
        'tag_chunks': tag_chunks,
        'doublets': doublets,
        'doublets_chunks': doublets_chunks,
        'triplets': triplets,
        'triplets_chunks': triplets_chunks
    }
    return render(request, 'app/index.html', context)


def generate_sequence(request, cat_ids='rand'):
    if cat_ids == 'rand':
        count = Tag.objects.count()
        rand_tag_id = Tag.objects.all()[randint(0, count - 1)].id
        tag_ids = [rand_tag_id]
    else:
        tag_ids = cat_ids.split(',')

    data = None
    for tag_id in tag_ids:
        if not data:
            data = FileTag.objects.filter(tag_id=tag_id).values_list('file__id', flat=True)
        else:
            next_data = FileTag.objects.filter(tag_id=tag_id).values_list('file__id', flat=True)
            # since MySQL doesn't support INTERSECT we need a workaround
            data = list(set(data) & set(next_data))
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
    file = File.objects.filter(id=file_id).first()
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
    files = File.objects.filter(needs_tagging=1).values()
    count = files.count()
    data = files[randint(0, count - 1)]
    tag_ids = FileTag.objects.filter(file_id=data['id']).values_list('tag__id', flat=True)
    data['files_tags'] = list(tag_ids)

    # prepare to load tags in Tagify format
    tags_tagify = []
    filetags = FileTag.objects.filter(file_id=data['id'])
    for filetag in filetags:
        tags_tagify.append({
            'id': filetag.tag.id,
            'value': filetag.tag.name.title()
        })
    data['files_tags_tagify'] = tags_tagify

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


def generate_doublets_triplets():
    # try cache first
    doublets_pickled = cache.get('doublets_pickled')
    triplets_pickled = cache.get('triplets_pickled')
    if doublets_pickled is None or triplets_pickled is None:
        # cache miss
        all_doublets = defaultdict(int)
        all_triplets = defaultdict(int)
        files = File.objects.all()
        for file in files:
            filetags = file.filetag_set.all()
            tagids = list(filetags.values_list('tag_id', flat=True))
            sorted(tagids)
            doublets = list(combinations(tagids, 2))
            triplets = list(combinations(tagids, 3))
            for doublet in doublets:
                commadoublet = ','.join(str(i) for i in doublet)
                all_doublets[commadoublet] += 1
            for triplet in triplets:
                commatriplet = ','.join(str(i) for i in triplet)
                all_triplets[commatriplet] += 1

        sorted_doublets = sorted(all_doublets, key=all_doublets.get, reverse=True)
        ready_doublets = {}
        for i in range(30):
            doublet_key = sorted_doublets[i]
            ready_doublets[doublet_key] = all_doublets[doublet_key]

        sorted_triplets = sorted(all_triplets, key=all_triplets.get, reverse=True)
        ready_triplets = {}
        for i in range(30):
            triplet_key = sorted_triplets[i]
            ready_triplets[triplet_key] = all_triplets[triplet_key]

        doublets_pickled = pickle.dumps(ready_doublets)
        triplets_pickled = pickle.dumps(ready_triplets)

        # cache will timeouts in 2 days
        timeout = 3600 * 24 * 2
        cache.set('doublets_pickled', doublets_pickled, timeout)
        cache.set('triplets_pickled', triplets_pickled, timeout)

    # cache is all set and we already have encoded results
    doublets_encoded = pickle.loads(doublets_pickled)
    triplets_encoded = pickle.loads(triplets_pickled)
    # {'2,30,31': 345, '7,22,23': 341, '18,30,31': 319, '22,23,24': 313, '7,22,24': 280}

    doublets = []
    for tags_commas, count in doublets_encoded.items():
        tag_ids = tags_commas.split(',')
        tag_names = list(Tag.objects.filter(id__in=tag_ids).values_list('name', flat=True))
        doublets.append({
            'tag_ids': tag_ids,
            'tag_names': tag_names,
            'count': count
        })
    triplets = []
    for tags_commas, count in triplets_encoded.items():
        tag_ids = tags_commas.split(',')
        tag_names = list(Tag.objects.filter(id__in=tag_ids).values_list('name', flat=True))
        triplets.append({
            'tag_ids': tag_ids,
            'tag_names': tag_names,
            'count': count
        })

    return doublets, triplets

# Create a function called "chunks" with two arguments, l and n:
def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]