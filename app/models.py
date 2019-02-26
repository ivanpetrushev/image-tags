from django.db import models

# Create your models here.


class File(models.Model):
    filename = models.CharField(max_length=255)
    last_viewed = models.DateTimeField()
    needs_tagging = models.BooleanField(default=False)
    cnt_views = models.IntegerField()
    created = models.DateTimeField()

    def __str__(self):
        return self.filename + ' at ' + self.created.strftime("%Y-%m-%d");

    class Meta:
        db_table = 'files'


class Tag(models.Model):
    name = models.CharField(max_length=255)
    navigation = models.CharField(max_length=1)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tags'


class FileTag(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'files_tags'
