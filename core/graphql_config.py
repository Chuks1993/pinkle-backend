import account.resolvers
import pinkle.resolvers
from ariadne import (
    MutationType,
    QueryType,
    load_schema_from_path,
    make_executable_schema,
    snake_case_fallback_resolvers,
)
from ariadne.contrib.django.scalars import date_scalar, datetime_scalar
from ariadne_jwt import GenericScalar, jwt_schema, resolve_refresh, resolve_verify

type_defs = [
    load_schema_from_path("core/schema.gql"),
    load_schema_from_path("pinkle/schema.gql"),
    load_schema_from_path("account/schema.gql"),
]

query = QueryType()
query.set_field("posts", pinkle.resolvers.resolve_posts)
query.set_field("post", pinkle.resolvers.resolve_post)

mutation = MutationType()
mutation.set_field("createPost", pinkle.resolvers.resolve_create_post)
mutation.set_field("deletePost", pinkle.resolvers.resolve_delete_post)

mutation.set_field("signupUser", account.resolvers.resolve_signup_user)

mutation.set_field("verifyToken", resolve_verify)
mutation.set_field("refreshToken", resolve_refresh)
mutation.set_field("tokenAuth", account.resolvers.resolve_token_auth)

schema = make_executable_schema(
    [*type_defs, jwt_schema],
    query,
    mutation,
    date_scalar,
    datetime_scalar,
    snake_case_fallback_resolvers,
    GenericScalar,
)
