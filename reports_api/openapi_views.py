from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


# Subclass drf-spectacular views to disable throttling (which requires Redis).
# Plain function wrappers prevent django-injector from trying to inject
# drf-spectacular's type-hinted parameters.

class _SchemaView(SpectacularAPIView):
    throttle_classes = []


class _SwaggerView(SpectacularSwaggerView):
    throttle_classes = []


class _RedocView(SpectacularRedocView):
    throttle_classes = []


_schema_view = _SchemaView.as_view()
_swagger_view = _SwaggerView.as_view(url_name='openapi-schema')
_redoc_view = _RedocView.as_view(url_name='openapi-schema')


def schema_view(request, *args, **kwargs):
    return _schema_view(request, *args, **kwargs)


def swagger_view(request, *args, **kwargs):
    return _swagger_view(request, *args, **kwargs)


def redoc_view(request, *args, **kwargs):
    return _redoc_view(request, *args, **kwargs)
