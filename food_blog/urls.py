"""
URL configuration for food_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from . import views  # Import the views module
from .views import like_comment, dislike_comment

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('terms/', views.terms_and_conditions, name='terms-and-conditions'),
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('topics/', views.TopicsListView.as_view(), name='topics-list'),
    path('topics/<slug:slug>/', views.TopicsDetailView.as_view(), name='topics-detail'),
    path('topics/<int:pk>/', views.TopicsDetailView.as_view(), name='topics-detail'),
    path('contest/', views.PhotoContestFormView.as_view(), name='contest'),
    path('comments/<int:pk>/like/', views.like_comment, name='like_comment'),
    path('comments/<int:pk>/dislike/', views.dislike_comment, name='dislike_comment'),
    path('like_comment/', views.like_comment, name="like"),
    path('dislike_comment', views.dislike_comment, name="dislike"),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico'))  # Favicon
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
