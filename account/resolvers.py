from ariadne import convert_kwargs_to_snake_case
from ariadne_jwt.decorators import login_required, token_auth
from graphql import GraphQLError

from account.models import User


@convert_kwargs_to_snake_case
@token_auth
def resolve_token_auth(obj, info, **kwargs):
    """Gets current current user from context and returns a user, token and refresh token"""
    print(info.context)
    user = info.context.get("request").user
    return {"user": user}


@convert_kwargs_to_snake_case
def resolve_signup_user(obj, info, input):
    """Takes an input dict consisting of email and password to sign up a new user then returns the user"""
    if User.objects.filter(email=input["email"]).exists():
        raise GraphQLError("This email already exists please try another email")
    # teacher = info.context.get("request").user
    user = User.objects.create_user(**input)
    user.save()
    return user


@convert_kwargs_to_snake_case
@login_required
def resolve_update_user(obj, info, input):
    current_user = info.context.get("request").user
    user = User.objects.get(pk=current_user.id)
    print(user, **input)
    # user.save(**input)
    return user


@login_required
def resolve_me(obj, info):
    return info.context.get("request").user
