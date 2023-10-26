# Generated by Django 3.2.5 on 2023-10-26 13:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0002_auto_20231026_0048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picturemodel',
            name='url',
        ),
        migrations.AddField(
            model_name='picturemodel',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='picturemodel',
            name='expiration_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='picturemodel',
            name='lat_1',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='picturemodel',
            name='lat_2',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='picturemodel',
            name='lon_1',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='picturemodel',
            name='lon_2',
            field=models.FloatField(null=True),
        ),
    ]
