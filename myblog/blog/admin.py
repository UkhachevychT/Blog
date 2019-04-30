from django.contrib import admin

from . import models

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created', 'modified',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'date',)

admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Comment, CommentAdmin)