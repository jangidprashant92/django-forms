"""
Home App Route
"""

from django.urls import path
from .views import life_form_view

urlpatterns = [
    path("", life_form_view, name="life_form_view"),
]
