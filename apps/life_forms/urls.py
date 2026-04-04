"""
Home App Route
"""

from collections import OrderedDict

from django.urls import path
from .views import CategoryListView, QuoteWizardView, life_form_view
from apps.life_forms.forms import FORM_REGISTRY

urlpatterns = [
    path("", life_form_view, name="life_form_view"),
    path("categories/", CategoryListView.as_view(), name="category_list"),
]

def add_wizard_route(product_key):
    steps = FORM_REGISTRY[product_key]
    form_list = [(s["slug"], s["form"]) for s in steps]
    urlpatterns.append(
        path(
            f"{product_key}/<slug:step>/",
            QuoteWizardView.as_view(
                form_list=form_list,
                url_name=f"quote_step_{product_key}",
                done_step_name="complete",
                steps_config=steps,
                product_type=product_key,
            ),
            name=f"quote_step_{product_key}",
        )
    )


for _product in FORM_REGISTRY.keys():
    add_wizard_route(_product)
