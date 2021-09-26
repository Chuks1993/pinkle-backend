from ariadne import convert_kwargs_to_snake_case
from ariadne_jwt.decorators import login_required
from django.db.models import F
from graphql import GraphQLError

from .models import Comment, Post


@convert_kwargs_to_snake_case
def resolve_posts(*_):
    """Returns all posts"""
    return Post.objects.all()


@convert_kwargs_to_snake_case
def resolve_post(self, info, post_id):
    """Returns Post based on post ID"""
    return Post.objects.get(pk=post_id)


@convert_kwargs_to_snake_case
def resolve_comments(self, info, post_id):
    return Comment.objects.filter(post=post_id)


@login_required
@convert_kwargs_to_snake_case
def resolve_update_post(self, info, post_id, input):
    """Takes post inputs and updates post accordingly"""
    author = info.context.get("request").user
    post = Post.objects.get(pk=post_id, author=author)
    if post.exist():
        raise GraphQLError("Not permitted to update this post")
    post.update(**input)
    return post


@convert_kwargs_to_snake_case
@login_required
def resolve_create_post(self, info, create_post_input):
    """Takes inputs consisting of title, body and description and more to creat eand return a post"""
    author = info.context.get("request").user
    post = Post.objects.create(**create_post_input, author=author)
    # post.likes.set(post.total_likes())
    return post


# @convert_kwargs_to_snake_case
# @login_required
# def resolve_toggle_like(self, info, post_id):
#     user = info.context.get("request").user
#     post = Post.objects.get(pk=post_id)
#     post.likes.add(user)
#     return True


@convert_kwargs_to_snake_case
@login_required
def resolve_toggle_like(self, info, comment_id):
    user = info.context.get("request").user
    post = Post.objects.get(pk=post_id)
    if post.favorites.filter(id=user.id).exists():
        post.favorites.remove(user)


# @convert_kwargs_to_snake_case
# @login_required
# def resolve_toggle_favorite(self, info, post_id):
#     user = info.context.get("request").user
#     post = Post.objects.get(pk=post_id)
#     liked = False
#     if post.exist():
#         if post.favorites.filter(id=user.id).exist():
#             post.update(favorites=F('favorites') - 1)
#         else:
#            post.update(favorites=F('favorites') - 1)
#         post.save()
#     return {"liked": liked}


@login_required
@convert_kwargs_to_snake_case
def resolve_delete_post(self, info, post_id):
    """Deletes post based on post ID"""
    author = info.context.get("request").user
    post = Post.objects.get(pk=post_id, author=author)
    if post.exist():
        raise GraphQLError("Not permitted to delete this post")
    post.delete()
    return True


# @login_required
# @convert_kwargs_to_snake_case
# def resolve_add_vote(self, info, post_id):
#     """Creates a vote for post"""
#     user = info.context.get("request").user
#     post = Post.objects.get(pk=post_id)
#     vote = Vote.objects.get(user=user, post=post)
#     if post.exist():
#         raise GraphQLError("User has already liked this post.")
#     Vote.objects.create(user=user, post=post, vote=True)
#     return True


@convert_kwargs_to_snake_case
@login_required
def resolve_add_comment(self, info, post_id, comment_input):
    user = info.context.get("request").user
    post = Post.objects.get(pk=post_id)
    try:
        comment = Comment.objects.create(**comment_input, user=user, post=post)
        return comment
    except Post.DoesNotExist:
        GraphQLError("Something went wrong. Cannot find post!")


@convert_kwargs_to_snake_case
@login_required
def resolve_remove_comment(self, info, comment_id):
    user = info.context.get("request").user
    comment = Comment.objects.get(pk=comment_id, author=user)
    try:
        comment.delete()
    except Comment.DoesNotExist:
        GraphQLError("You dont't have the permission to delete this comment")


@convert_kwargs_to_snake_case
@login_required
def resolve_update_comment(self, info, comment_id, comment_input):
    user = info.context.get("request").user
    comment = Comment.objects.get(pk=comment_id, author=user)
    try:
        comment.update(**comment_input)
    except Comment.DoesNotExist:
        GraphQLError("You don't have permission to update this posts!")


def resolve_trending_posts(self, info):
    return Post.objects.all().order_by("-votes")


# @convert_kwargs_to_snake_case
# @login_required
# def resolve_like(self, info, post_id):
#     user = info.context.get("request").user
#     post = Post.objects.get(pk=post_id)
#     liked = False
#     like = Like.objects.filter(user=user, post=post)
#     if like:
#         like.delete()
#     else:
#         liked = True
#         Like.objects.create(user=user, post=post)
#     return {"liked": liked}
