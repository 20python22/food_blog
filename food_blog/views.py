"""
All the Django views are in this file.
"""


# food_blog/views.py

from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Count
from django.db.models import Subquery
from . import models


def index(_request):
    """
    Http response.
    """
    return HttpResponse('Hello world!')


def home(request):
    # Get last 10 posts
    latest_posts = models.Post.objects.order_by('-published')[:10]

    # Get topics related to the latest 10 posts
    topic_numbers = models.Topic.objects.filter(
        post__in=Subquery(latest_posts.values('id')),
    ).annotate(
        post_count=Count('post', distinct=True),
    )
    popular_topics = topic_numbers.order_by('-post_count')
    # Add as context variables
    context = {
        'latest_posts': latest_posts,
        'popular_topics': popular_topics,
    }
    return render(request, 'food_blog/home.html', context)
