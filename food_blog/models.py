""" food_blog/models.py """

# The pylint warning about class meta having too few public methods is a bug in pylint.
# https://github.com/pylint-dev/pylint-django/issues/367

from django.db import models
from django.conf import settings
from django.urls import reverse


class Topic(models.Model):
    """
    Represents a topic post
    """
    objects = None  # This is required to fix pylint error Unresolved attribute reference
    # 'objects' for class 'Topic'
    name = models.CharField(
        max_length=50,
        blank=False,
        null=False
    )
    slug = models.SlugField(
        blank=False,
        null=False
    )

    def get_absolute_url(self):
        """Slug definition"""
        return reverse("article_detail", kwargs={"slug": self.slug})  # new

    def __str__(self):
        return str(self.name)


class Post(models.Model):
    """
    Represents a blog post
    """
    objects = None  # This is required to fix pylint error Unresolved attribute reference
    # 'objects' for class 'Post'
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
        related_name='user',
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
        help_text='Set to "Published" to make this post publicly visible',
        blank=False,
        null=False
    )
    published = models.DateTimeField(
        auto_now_add=True,
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


class Comment(models.Model):
    """
    Represents a comment post
    """
    objects = None  # This is required to fix pylint error Unresolved attribute
    # reference 'objects' for class 'Comment'
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

    class Meta:
        """Ordering by created"""
        ordering = ['-created']

    def __str__(self):
        return str(self.post)
