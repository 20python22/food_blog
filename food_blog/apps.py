"""Apps"""

from django.apps import AppConfig


class FoodBlogConfig(AppConfig):
    """BlogConfig"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'food_blog'
