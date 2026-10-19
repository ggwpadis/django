from django.contrib import admin
from .models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'likes', 'created_at')
    search_fields = ('title', 'author')
    list_filter = ('created_at',)