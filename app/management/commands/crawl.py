import os
import subprocess
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from app.models import File


class Command(BaseCommand):
    root_dir = '/images'

    def handle(self, *args, **options):
        extensions = ['jpg', 'jpeg', 'png', 'gif']

        # find last created file
        last_created = File.objects.order_by('-created').first()

        # calculate how many days ago was it created
        ts_modified = os.path.getmtime(self.root_dir + last_created.filename)
        ts_modified = datetime.fromtimestamp(ts_modified)
        ts_now = datetime.now()
        ts_delta = ts_now - ts_modified
        diff_days = abs(ts_delta).days
        print('Diff days:', diff_days)

        # find any files created from that date onwards
        cmd = "find " + self.root_dir + " -mtime -" + str(diff_days)
        result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
        files = result.stdout.decode().split()
        for i in range(len(files)):
            filename = str(files[i])
            filename_relative = filename.replace(self.root_dir, '')
            extension = os.path.splitext(filename)[1][1:]
            # if file has correct extension and does not exist in DB, save it
            if extension not in extensions:
                continue
            file_exists = File.objects.filter(filename=filename_relative).count()
            if file_exists:
                continue
            print('adding', filename_relative)

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record = File(filename=filename_relative, created=now, last_viewed=now, needs_tagging=1, cnt_views=0)
            record.save()
        return 'done'
