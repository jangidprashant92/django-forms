"""
Home App Route
"""

from django.urls import path
from .views import step1, step2, coverage_options, claims_section, decline_section

urlpatterns = [
    path("", step1, name="step1"),
    path("step2/", step2, name="step2"),
    path("coverage-options/", coverage_options),
    path("claims-section/", claims_section),
    path("decline-section/", decline_section),
]
