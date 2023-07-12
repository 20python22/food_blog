"""
All the Django views are in this file.
"""

# food_blog/views.py

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from . import models


class Home(TemplateView):
    template_name = 'food_blog/home.html'


class AboutView(TemplateView):
    template_name = 'food_blog/about.html'


def terms_and_conditions(request):
    return render(request, 'food_blog/terms_and_conditions.html')


class PostListView(ListView):
    model = models.Post
    context_object_name = 'posts'
    queryset = models.Post.objects.published().order_by('-published')


class PostDetailView(DetailView):
    model = models.Post

    def get_queryset(self):
        queryset = super().get_queryset()

        # If this is a `pk` lookup, use default queryset
        if 'pk' in self.kwargs:
            return queryset

        # Otherwise, filter on the published date
        return queryset.filter(
            published__year=self.kwargs['year'],
            published__month=self.kwargs['month'],
            published__day=self.kwargs['day'],
        )


class TopicsListView(ListView):
    model = models.Topic
    context_object_name = 'topics'
    queryset = models.Topic.objects.order_by('name')


class TopicsDetailView(DetailView):
    model = models.Topic

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        topic = get_object_or_404(models.Topic, slug=slug)

        return topic
