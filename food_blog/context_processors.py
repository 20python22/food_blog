# food_blog/context_processors.py

from . import models
from django.db.models import Count
from django.db.models import Subquery
from django.contrib.auth.models import User


def base_context(request):
    # authors = models.Post.objects.published().get_authors().order_by('first_name')

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
    return context


def unique_author_names(request):
    author_names = User.objects.values_list('first_name', 'last_name').distinct()
    return {'unique_author_names': author_names}
