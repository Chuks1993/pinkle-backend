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
            GraphQLView.as_view(
                schema=schema,
                playground_options={"settings": {"request.credentials": "include"}},
                validation_rules=[cost_validator(maximum_cost=5, default_complexity=1)],
            )
        ),
        name="graphql",
    ),
]

# https://spectrum.chat/ariadne/general/request-data-and-cookies-using-asgi-django-channels~ab4e8cd4-4d33-4d3c-ac4a-f0936a61a5f7
