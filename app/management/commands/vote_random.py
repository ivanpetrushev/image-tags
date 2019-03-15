import os
import subprocess
from random import shuffle
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from app.models import File


class Command(BaseCommand):
    root_dir = '/images'

    def handle(self, *args, **options):
        file_ids = list(File.objects.values_list('id', flat=True))
        shuffle(file_ids)
        file_ids = file_ids[:20]
        print(file_ids)
        File.objects.filter(id__in=file_ids).update(needs_tagging=1)
        return 'done'
