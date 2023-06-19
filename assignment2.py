"""Assignment 2 query answers"""

from django.contrib.auth import get_user_model
from django.db.models import Sum

from food_blog.models import Comment, Post

User = get_user_model()


def question_1_return_active_users():
    """
    Return the results of a query which returns a list of all
    active users in the database.
    """
    return get_user_model().objects.filter(is_active=True)
    # Output example: <QuerySet [<User: admin>, <User: superuser>]>


print(question_1_return_active_users())


def question_2_return_regular_users():
    """
    Return the results of a query which returns a list of users that
    are *not* staff and *not* superusers
    """
    return get_user_model().objects.filter(is_staff=False, is_superuser=False)
    # Output example: <QuerySet [<User: John>, <User: Joe>]>


print(question_2_return_regular_users())


def question_3_return_all_posts_for_user(user):
    """
    Return all the Posts authored by the user provided. Posts should
    be returned in reverse chronological order from when they
    were created.
    """
    return Post.objects.filter(author=user).order_by('-created')


users = User.objects.get(username='Joe')
posts = question_3_return_all_posts_for_user(users)
for post_titles in posts:
    print(post_titles.title)
# Output example: Good fries toppings, How fries is made


def question_4_return_all_posts_ordered_by_title():
    """
    Return all Post objects, ordered by their title.
    """
    return Post.objects.all().order_by('title')
    # Added Objects = None to Post class to fix Pylint
    # error Unresolved attribute reference 'objects' for class 'Post'
    # Output example: <QuerySet [<Post: Good burger toppings>, <Post: Good fries toppings>]>


print(question_4_return_all_posts_ordered_by_title())


def question_5_return_all_post_comments(post):
    """
    Return all the comments made for the post provided in order
    of last created.
    """
    comments_all = Comment.objects.filter(post=post).order_by('-created').\
        values_list('text', flat=True)
    return comments_all


posts = Post.objects.get(id=2)
comments = question_5_return_all_post_comments(posts)
print(comments)
# Output example: <QuerySet ['Yes it is.', 'No it is not.']>


def question_6_return_the_post_with_the_most_comments():
    """
    Return the Post object containing the most comments in
    the database. Do not concern yourself with approval status;
    return the object which has generated the most activity.
    """
    return Post.objects.annotate(num_comments=Sum('comments__id', distinct=True))\
        .order_by('-num_comments').first()
    # Output example: <Post: What food is best>


print(question_6_return_the_post_with_the_most_comments())


def question_7_create_a_comment(post):
    """
    Create and return a comment for the post object provided.
    """
    comment_return = Comment.objects.create(post=post, text='Lorem ipsum dolor sit amet.')
    return comment_return
    # Added Objects = None to Post class to fix Pylint


posts = Post.objects.get(id=2)
comments = question_7_create_a_comment(posts)
print(comments)
# Output example: Is pizza the best


def question_8_set_approved_to_false(comment):
    """
    Update the comment record provided and set approved=False
    """
    comment_update = Comment.objects.get(id=comment)
    comment_update.approved = False
    comment_update.save()
    return comment_update


comment_updated = question_8_set_approved_to_false(9)
print(comment_updated)
# Output example: What food is best


def question_9_delete_post_and_all_related_comments(post):
    """
    Delete the post object provided, and all related comments.
    """
    comment_delete = Comment.objects.filter(post=post)
    comment_delete.delete()
    post.delete()
    return 'deleted post'


post_to_delete = Post.objects.get(id=2)
deleted = question_9_delete_post_and_all_related_comments(post_to_delete)
print(deleted)
# Output example: Is pizza the best
