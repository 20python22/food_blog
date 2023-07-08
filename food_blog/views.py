"""
All the Django views are in this file.
"""

# food_blog/views.py

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView
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
