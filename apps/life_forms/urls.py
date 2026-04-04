"""
Home App Route
"""

from django.urls import path
from apps.life_forms.forms import FORM_REGISTRY
from .views import QuoteWizardView, QuoteListView
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="life_form_view"),
    path("quotes/", QuoteListView.as_view(), name="quote_list"),
    path(
        "<str:product_type>/<slug:step>/",
        QuoteWizardView.as_view(
            url_name="quote_step",
            done_step_name="complete",
            # Provide a placeholder form_list to satisfy formtools assertion; real list is built dynamically.
            form_list=[("init", list(FORM_REGISTRY.values())[0][0]["form"])],
        ),
        name="quote_step",
    ),
]
