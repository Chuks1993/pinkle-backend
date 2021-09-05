from ariadne.contrib.django.views import GraphQLView
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .graphql_config import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "graphql/",
        csrf_exempt(
            GraphQLView.as_view(
                schema=schema,
            )
        ),
        name="graphql",
    ),
]
