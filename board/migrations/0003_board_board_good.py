# Generated by Django 3.2.9 on 2021-12-17 02:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0002_boardcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='board_good',
            field=models.ManyToManyField(blank=True, related_name='board_good', to=settings.AUTH_USER_MODEL),
        ),
    ]
