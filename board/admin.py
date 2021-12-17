from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Board


class BoardModelAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = ('content',)


# Register your models here.
admin.site.register(Board, BoardModelAdmin)