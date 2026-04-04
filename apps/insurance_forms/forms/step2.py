from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, HTML, ButtonHolder, Submit


class Step2PlanForm(forms.Form):

    CARE_TYPE_CHOICES = [
        ("basic", "Basic Care"),
        ("premium", "Premium Care"),
    ]

    PLAN_CHOICES = [
        ("p1", "Plan 1"),
        ("p2", "Plan 2"),
        ("p3", "Plan 3"),
    ]

    # Shown only if coverage == comprehensive
    care_type = forms.ChoiceField(
        choices=CARE_TYPE_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label="Care Type",
    )

    plan = forms.ChoiceField(
        choices=PLAN_CHOICES, widget=forms.RadioSelect, label="Select a Plan"
    )

    # Shown only if coverage == basic
    building = forms.IntegerField(required=False, label="Building (SGD)")
    renovation = forms.IntegerField(required=False, label="Renovation (SGD)")
    contents = forms.IntegerField(required=False, label="Contents (SGD)")

    LIABILITY_CHOICES = [
        ("0", "No Top-up"),
        ("1m", "SGD 1 million"),
        ("1_5m", "SGD 1.5 million"),
        ("2m", "SGD 2 million"),
    ]

    liability_topup = forms.ChoiceField(
        choices=LIABILITY_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label="Top up Personal Liability?",
    )

    def __init__(self, *args, **kwargs):
        print("================================")
        print(kwargs)
        coverage = kwargs.pop("coverage")
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.render_unmentioned_fields = False

        # === COMMON LAYOUT ===
        layout_items = [
            HTML('<h2 class="text-xl font-semibold mb-4">Step 2 of 3 – Plans</h2>')
        ]

        # === IF COMPREHENSIVE ===
        if coverage == "comprehensive":
            layout_items += [
                Fieldset(
                    "Care Selection",
                    "care_type",
                ),
                Fieldset(
                    "Available Plans",
                    "plan",
                ),
            ]

        # === IF BASIC NAMED PERILS ===
        else:
            layout_items += [
                Fieldset(
                    "Coverage Amounts",
                    "building",
                    Div(
                        "liability_topup",
                        css_class="mt-4",
                    ),
                    "renovation",
                    "contents",
                )
            ]

        # === ACTIONS ===
        layout_items += [
            ButtonHolder(
                HTML(
                    '<a href="/insurance_forms/" class="btn btn-secondary mr-4">Back</a>'
                ),
                Submit("next", "Next", css_class="btn btn-primary"),
            )
        ]

        self.helper.layout = Layout(*layout_items)
