# Generated by Django 3.2.9 on 2021-12-01 17:27

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_alter_post_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=markdownx.models.MarkdownxField(),
        ),
    ]
