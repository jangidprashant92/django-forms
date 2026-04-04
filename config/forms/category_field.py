from django import forms

from apps.life_forms.models import Category
from config.forms.widgets import CategorySelectWidget


class CategoryChoiceField(forms.ModelChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs["queryset"] = Category.objects.filter(is_active=True).only("id", "name")
        kwargs.setdefault("empty_label", "Select Cat")
        kwargs.setdefault("widget", CategorySelectWidget())
        super().__init__(*args, **kwargs)
