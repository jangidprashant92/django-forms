from django.forms.widgets import Select


class CategorySelectWidget(Select):
    template_name = "widgets/category_select.html"

    def __init__(self, attrs=None):
        default_attrs = {"class": "w-[50%]", "pj": "pj-true"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

    def render(self, name, value, attrs=None, renderer=None):
        print(">>> CUSTOM WIDGET RENDER EXECUTED <<<")
        return super().render(name, value, attrs, renderer)
