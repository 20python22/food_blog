""" food_blog/models.py """

# The pylint warning about class meta having too few public methods is a bug in pylint.
# https://github.com/pylint-dev/pylint-django/issues/367

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User


class Topic(models.Model):
    """
    Represents a topic post
    """
    objects = None
    name = models.CharField(
        max_length=50,
        blank=False,
        null=False
    )
    slug = models.SlugField(
        blank=False,
        null=False,
        unique=True
    )

    def get_absolute_url(self):
        """Slug definition"""
        kwargs = {
            'slug': self.slug
        }
        return reverse("topics-detail", kwargs=kwargs)  # new

    def __str__(self):
        return str(self.name)


class PublishedManager(models.Manager):
    def published(self):
        return self.filter(status='published')

    def get_authors(self):
        return User.objects.filter(posts__status='published').distinct()


class Post(models.Model):
    """
    Represents a blog post
    """
    objects = PublishedManager()

    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'draft'),
        (PUBLISHED, 'published')
    ]

    title = models.CharField(
        max_length=150,
        blank=False,
        null=False
    )
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # The Django auth user model
        on_delete=models.PROTECT,  # Prevent posts from being deleted
        related_name='posts',
        blank=False,
        null=False
    )
    created = models.DateTimeField(
        auto_now_add=True  # Sets on create
    )
    updated = models.DateTimeField(
        auto_now=True  # Updates on each save
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text='Set to "Published" to make this post publicly visible. If the post is set to Draft'
                  'it will not display on the site',
        blank=False,
        null=False
    )
    published = models.DateTimeField(
        verbose_name='date published'
    )
    slug = models.SlugField(
        unique_for_date='published',
        blank=False,
        null=False
    )
    topics = models.ManyToManyField(Topic)

    class Meta:
        """Ordering by created"""
        ordering = ['-created']

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        if self.published:
            kwargs = {
                'year': self.published.year,
                'month': self.published.month,
                'day': self.published.day,
                'slug': self.slug
            }
        else:
            kwargs = {'pk': self.pk}

        return reverse('post-detail', kwargs=kwargs)


class Comment(models.Model):
    """
    Represents a comment post
    """
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='comments',
        blank=False
    )
    name = models.CharField(
        max_length=50,
        blank=False
    )
    email = models.CharField(
        max_length=100,
        blank=False
    )
    text = models.TextField(
        max_length=500,
        blank=False
    )
    approved = models.BooleanField(
        null=True
    )
    created = models.DateTimeField(
        auto_now_add=True  # Sets on create
    )
    updated = models.DateTimeField(
        auto_now=True  # Updates on each save
    )

    def __str__(self):
        return str(self.post)
