from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Row,
    Column,
    Div,
    ButtonHolder,
    Submit,
    HTML,
)


def input_group_layout(label_name: str, fields):
    return Div(
        Column(
            HTML(
                f"<label class='text-lg font-bold text-gray-700 text-right'>{label_name}</label>"
            ),
            css_class="col-span-1",
        ),
        Column(
            fields,
            css_class="col-span-1",
        ),
        css_class="grid grid-cols-3 items-top gap-4",
    )


def radio_input_layout(field_name: str):
    return HTML(
        f"""
                        <div class="grid grid-rows-2 gap-2">
                            {{% for radio in form.{field_name} %}}
                                <label
                                    class="p-2 rounded-lg bg-white border-grey-100 border-[1px]
                                        cursor-pointer flex items-center gap-2"
                                >
                                    {{{{ radio.tag }}}}
                                    <p class="text-gray-400">{{{{ radio.choice_label }}}}</p>
                                </label>
                            {{% endfor %}}
                        </div>
                        """
    )


class Step1InsuranceForm(forms.Form):

    given_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Given name"}),
    )
    family_name = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "Family name"})
    )

    COVERAGE_CHOICES = [
        ("basic", "Basic – Named Perils"),
        ("comprehensive", "Comprehensive – All Risk"),
    ]
    coverage = forms.ChoiceField(
        label="",
        choices=COVERAGE_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "flex gap-6 items-center"}),
    )

    coverage_period = forms.ChoiceField(
        label="Coverage Period",
        choices=[
            ("12", "12 Months"),
            ("24", "24 Months (5% discount)"),
        ],
        widget=forms.RadioSelect,
        required=False,
    )

    personal_effects = forms.ChoiceField(
        label="Personal Effects / Valuables?",
        choices=[("yes", "Yes"), ("no", "No")],
        widget=forms.RadioSelect,
        required=False,
    )

    occupancy = forms.ChoiceField(
        label="",
        choices=[
            ("landlord", "Landlord"),
            ("tenant", "Tenant"),
            ("owner", "Owner Occupier"),
        ],
        widget=forms.RadioSelect,
    )

    property_type = forms.ChoiceField(
        label="",
        choices=[
            ("hob", "HOB"),
            ("semi", "Semi-detached"),
            ("other", "Others"),
        ],
    )

    postal_code = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Postal Code"}),
    )

    use_of_property = forms.ChoiceField(
        label="",
        choices=[
            ("res", "Residential"),
            ("non", "Non-Residential"),
        ],
        widget=forms.RadioSelect,
    )

    has_claims = forms.ChoiceField(
        label="",
        choices=[("yes", "Yes"), ("no", "No")],
        widget=forms.RadioSelect,
    )

    claim_count = forms.IntegerField(required=False, min_value=1)
    claim_amount = forms.IntegerField(required=False, min_value=1)

    declined_before = forms.ChoiceField(
        label="",
        choices=[("yes", "Yes"), ("no", "No")],
        widget=forms.RadioSelect,
    )

    decline_reason = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "space-y-8"
        self.helper.label_class = "w-1/3 font-semibold"

        self.helper.layout = Layout(
            input_group_layout(
                "Policy Holder Name",
                Row(
                    Column("given_name"),
                    Column("family_name"),
                    css_class="grid grid-rows-2 gap-4",
                ),
            ),
            input_group_layout(
                "Coverage",
                Row(
                    radio_input_layout("coverage"),
                    hx_post="/insurance_forms/coverage-options/",
                    hx_trigger="change",
                    hx_target="#coverage-options",
                    css_class="mb-3 gap-6",
                ),
            ),
            Div(id="coverage-options"),
            input_group_layout(
                "Occupancy",
                Row(
                    radio_input_layout("occupancy"),
                    css_class="mb-3 gap-6",
                ),
            ),
            input_group_layout(
                "Type of Property",
                Row(
                    "property_type",
                    css_class="w-full text-gray-400",
                ),
            ),
            input_group_layout(
                "Insured Premises",
                Row(
                    "postal_code",
                    css_class="w-full text-gray-400",
                ),
            ),
            input_group_layout(
                "Use of Property",
                Row(
                    radio_input_layout("use_of_property"),
                    css_class="mb-3 gap-6",
                ),
            ),
            input_group_layout(
                "Claims in last 3 years?",
                Row(
                    radio_input_layout("has_claims"),
                    css_class="mb-3 gap-6",
                    hx_post="/insurance_forms/claims-section/",
                    hx_trigger="change",
                    hx_target="#claims-section",
                ),
            ),
            Div(id="claims-section"),
            input_group_layout(
                "Proposal ever declined?",
                Row(
                    radio_input_layout("declined_before"),
                    css_class="mb-3 gap-6",
                    hx_post="/insurance_forms/decline-section/",
                    hx_trigger="change",
                    hx_target="#decline-section",
                ),
            ),
            Div(id="decline-section"),
            ButtonHolder(
                Submit(
                    "next",
                    "Next",
                    css_class=(
                        "inline-flex items-center justify-center "
                        "px-6 py-2 text-sm font-semibold text-white "
                        "bg-blue-600 hover:bg-blue-700 "
                        "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 "
                        "rounded-md transition"
                    ),
                )
            ),
        )
