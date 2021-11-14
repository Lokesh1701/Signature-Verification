from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(r"", include(("verifyApp.urls", "verifyApp"), namespace="api")),
]
