from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout

from config.forms.category_field import CategoryChoiceField


class LifeForm(forms.Form):
    category = CategoryChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field(
                "category",
                # template="widgets/category_select.html",  # ✅ force template
                css_class="w-[50%]",  # ✅ crispy-safe styling
            ),
        )
