from django.contrib import admin

from . import models

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created', 'modified',)

admin.site.register(models.Post, PostAdmin)
