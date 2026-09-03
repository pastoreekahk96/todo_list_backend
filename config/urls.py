"""URL configuration for the Todo API project."""

from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def api_home(request):
    """Return a simple response from the API root."""
    return JsonResponse(
        {
            "message": "Welcome to the Todo API.",
            "backend": "Pastoreekahk S Arthur",
            "frontend": "Joseph Banda",
        }
    )


urlpatterns = [
    path("", api_home, name="api-home"),
    path("admin/", admin.site.urls),
    path("api/", include("todo.urls")),
]
