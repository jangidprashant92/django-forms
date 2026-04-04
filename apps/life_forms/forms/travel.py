from django import forms
from apps.life_forms.forms.base import BaseQuoteForm

class TravelDetailsForm(BaseQuoteForm):
    destination = forms.CharField()
    travel_date = forms.DateField()


class TravelPersonForm(BaseQuoteForm):
    age = forms.IntegerField()
    passport = forms.CharField()