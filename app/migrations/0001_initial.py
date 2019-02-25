# Generated by Django 2.1.7 on 2019-02-25 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=255)),
                ('last_viewed', models.DateTimeField()),
                ('needs_tagging', models.BooleanField(default=False)),
                ('cnt_views', models.IntegerField()),
                ('created', models.DateTimeField()),
            ],
            options={
                'db_table': 'files',
            },
        ),
        migrations.CreateModel(
            name='FileTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.File')),
            ],
            options={
                'db_table': 'files_tags',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('navigation', models.CharField(max_length=1)),
            ],
            options={
                'db_table': 'tags',
            },
        ),
        migrations.AddField(
            model_name='filetag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Tag'),
        ),
    ]
