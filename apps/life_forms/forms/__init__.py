from django import forms

from .base import BaseQuoteForm
from .travel import TravelDetailsForm, TravelPersonForm


class ReviewForm(forms.Form):
    """Final confirmation step; stays empty by design."""

    confirm = forms.BooleanField(required=False, initial=True, widget=forms.HiddenInput())


class EventDetailsForm(BaseQuoteForm):
    event_name = forms.CharField()
    event_date = forms.DateField()


class EventPersonForm(BaseQuoteForm):
    attendee_name = forms.CharField()
    tickets = forms.IntegerField()


class HomeGuardDetailsForm(BaseQuoteForm):
    property_address = forms.CharField()
    coverage_start = forms.DateField()


class HomeGuardPersonForm(BaseQuoteForm):
    occupants = forms.IntegerField()
    alarm_system = forms.BooleanField(required=False)


FORM_REGISTRY = {
    "travel": [
        {"slug": "details", "form": TravelDetailsForm, "template": "quote/wz_form.html"},
        {"slug": "person", "form": TravelPersonForm, "template": "quote/wz_form.html"},
        {"slug": "review", "form": ReviewForm, "template": "quote/review.html"},
    ],
    "event": [
        {"slug": "details", "form": EventDetailsForm, "template": "quote/wz_form.html"},
        {"slug": "person", "form": EventPersonForm, "template": "quote/wz_form.html"},
        {"slug": "review", "form": ReviewForm, "template": "quote/review.html"},
    ],
    "home-guard": [
        {"slug": "details", "form": HomeGuardDetailsForm, "template": "quote/wz_form.html"},
        {"slug": "person", "form": HomeGuardPersonForm, "template": "quote/wz_form.html"},
        {"slug": "review", "form": ReviewForm, "template": "quote/review.html"},
    ],
}

__all__ = [
    "BaseQuoteForm",
    "TravelDetailsForm",
    "TravelPersonForm",
    "EventDetailsForm",
    "EventPersonForm",
    "HomeGuardDetailsForm",
    "HomeGuardPersonForm",
    "ReviewForm",
    "FORM_REGISTRY",
]
