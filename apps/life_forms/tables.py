import django_tables2 as tables
from .models import Category

class CategoryTable(tables.Table):
    class Meta:
        model = Category
        template_name = "tables/tailwind.html"  # custom template
        fields = ("name", "is_active")
        attrs = {
            "class": "min-w-full divide-y divide-gray-200"
        }