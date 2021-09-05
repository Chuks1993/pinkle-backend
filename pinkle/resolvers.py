from ariadne import convert_kwargs_to_snake_case
from ariadne_jwt.decorators import login_required
from graphql import GraphQLError

from .models import Post


@convert_kwargs_to_snake_case
def resolve_posts(*_):
    """Returns all posts"""
    return Post.objects.all()


@convert_kwargs_to_snake_case
def resolve_post(self, info, post_id):
    """Returns Post based on post ID"""
    return Post.objects.get(pk=post_id)


@login_required
@convert_kwargs_to_snake_case
def resolve_update_post(self, info, post_id, input):
    """Takes post inputs and updates post accordingly"""
    author = info.context.get("request").user
    post = Post.objects.get(pk=post_id)
    if post.author.id != author.id:
        raise GraphQLError("Not permitted to update this post")
    post.update(**input)
    return post


@login_required
def resolve_create_post(self, info, input):
    """Takes inputs consisting of title, body and description and more to creat eand return a post"""
    author = info.context.get("request").user
    post = Post.objects.create(**input, author=author)
    return post


@login_required
@convert_kwargs_to_snake_case
def resolve_delete_post(self, info, post_id):
    """Deletes post based on post ID"""
    author = info.context.get("request").user
    post = Post.objects.get(pk=post_id)
    if post.author.id != author.id:
        raise GraphQLError("Not permitted to delete this post")
    post.delete()
    return True
