"""Admin"""

from django.contrib import admin
from . import models


class CommentInLine(admin.StackedInline):
    """Comment InLine class"""
    model = models.Comment
    extra = 0
    fields = ('name', 'email', 'text', 'approved')
    readonly_fields = ('name', 'email', 'text')


class CommentAdmin(admin.ModelAdmin):
    """Comment class"""
    list_display = (
        'name',
        'email',
        'text',
        'created',
        'updated',
        'approved'
    )

    search_fields = (
        'name',
        'email',
        'text'
    )

    list_filter = (
        'approved',
    )


admin.site.register(models.Comment, CommentAdmin)


class PostAdmin(admin.ModelAdmin):
    """Admin class"""
    list_display = (
        'title',
        'author',
        'status',
        'created',
        'updated',
    )

    search_fields = (
        'title',
        'author__username',
        'author__first_name',
        'author__last_name',
    )

    list_filter = (
        'status',
        'topics'
    )

    inlines = [
        CommentInLine,
    ]


admin.site.register(models.Post, PostAdmin)


class TopicAdmin(admin.ModelAdmin):
    """Admin class"""
    list_display = (
        'name',
        'slug'
    )


admin.site.register(models.Topic, TopicAdmin)
