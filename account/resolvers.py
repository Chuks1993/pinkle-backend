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
    """Takes an input dict consisting of email, username and password to sign up a new user then returns the user"""
    if User.objects.filter(email=input["email"]).exists():
        raise GraphQLError("This email already exists please try another email")
    user = User.objects.create_user(**input)
    user.save()
    return user
