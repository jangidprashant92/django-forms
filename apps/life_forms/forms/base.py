from django import forms
from apps.life_forms.models import Test


class BaseQuoteForm(forms.ModelForm):
    """Base form that automatically splits structured and dynamic data."""

    class Meta:
        model = Test
        fields = ["quote_num", "customer_name", "customer", "product_type"]

    def __init__(self, *args, **kwargs):
        product_type = kwargs.pop("product_type", None)
        super().__init__(*args, **kwargs)

        # keep product_type out of the UI while ensuring it is persisted
        if "product_type" in self.fields:
            self.fields["product_type"].widget = forms.HiddenInput()
            initial_value = product_type or getattr(self.instance, "product_type", None)
            if initial_value:
                self.initial.setdefault("product_type", initial_value)

        # hide internal tracking fields
        for hidden_field in ("customer",):
            if hidden_field in self.fields:
                self.fields[hidden_field].widget = forms.HiddenInput()

    def save(self, commit: bool = True, instance=None):
        if instance:
            self.instance = instance

        instance = super().save(commit=False)

        model_fields = set(self.Meta.fields)
        json_data = {}

        for field, value in self.cleaned_data.items():
            if field in model_fields or value in [None, ""]:
                continue

            # Coerce non-JSON-serializable values (e.g., date/datetime) to strings
            if hasattr(value, "isoformat"):
                value = value.isoformat()

            json_data[field] = value

        instance.details = {
            **(instance.details or {}),
            **json_data,
        }

        if commit:
            instance.save()

        return instance
