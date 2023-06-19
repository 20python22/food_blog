"""
All the Django views are in this file.
"""


# food_blog/views.py

from django.http import HttpResponse
from django.shortcuts import render


def index(_request):
    """
    Http response.
    """
    return HttpResponse('Hello world!')
