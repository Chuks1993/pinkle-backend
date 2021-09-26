from ariadne.contrib.django.views import GraphQLView
from ariadne.validation import cost_validator
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .graphql_config import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "graphql/",
        csrf_exempt(
            GraphQLView.as_view(schema=schema, validation_rules=[cost_validator(maximum_cost=5, default_complexity=1)])
        ),
        name="graphql",
    ),
]
