from django.contrib import admin
from .models import Post, Category, Tag

admin.site.register(Post)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )} # name 필드에 값이 입력됐을 때 자동으로 slug가 만들어진다.


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)