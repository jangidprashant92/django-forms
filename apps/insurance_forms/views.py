from crispy_forms.layout import Layout, Row, Div
from crispy_forms.helper import FormHelper
from django.shortcuts import redirect, render

from .forms.step1 import Step1InsuranceForm, input_group_layout, radio_input_layout
from .forms.step2 import Step2PlanForm


def step1(request):
    step1_data = request.session.get("step1")
    form = Step1InsuranceForm(request.POST or step1_data or None)

    if request.method == "POST" and form.is_valid():
        print(form.cleaned_data)
        request.session["step1"] = form.cleaned_data
        return redirect("step2")

    return render(request, "step1.html", {"form": form})


def step2(request):
    step1 = request.session.get("step1")

    if not step1 or "coverage" not in step1:
        return redirect("step1")

    coverage = step1["coverage"]

    if request.method == "POST":
        form = Step2PlanForm(request.POST, coverage=coverage)
        if form.is_valid():
            request.session["step2"] = form.cleaned_data
            return redirect("step3")
    else:
        form = Step2PlanForm(coverage=coverage)

    return render(request, "step2.html", {"form": form})


def coverage_options(request):
    # form = Step1InsuranceForm(request.POST)
    # return render(
    #     request,
    #     "partials/coverage_options.html",
    #     {"form": form, "coverage": request.POST.get("coverage")},
    # )
    coverage = request.POST.get("coverage")

    form = Step1InsuranceForm(request.POST or None)

    helper = FormHelper()
    helper.form_tag = False  # VERY IMPORTANT for HTMX partials
    helper.form_class = "space-y-8"

    if coverage == "basic":
        helper.layout = Layout(
            Div(
                input_group_layout(
                    "Coverage Period",
                    Row(
                        radio_input_layout("coverage_period"),
                        css_class="mb-3 gap-6",
                    ),
                ),
                css_class="flex flex-col",
            ),
        )

    elif coverage == "comprehensive":
        helper.layout = Layout(
            Div(
                input_group_layout(
                    "Coverage Period",
                    Div(
                        radio_input_layout("coverage_period"),
                        css_class="mb-3",
                    ),
                ),
                css_class="flex flex-col",
            ),
            Div(
                input_group_layout(
                    "Personal Effects",
                    Row(
                        radio_input_layout("personal_effects"),
                        css_class="mb-3 gap-6",
                    ),
                ),
                css_class="flex flex-col",
            ),
        )
    else:
        helper.layout = Layout()

    return render(
        request,
        "partials/coverage_options.html",
        {
            "form": form,
            "helper": helper,
        },
    )


def claims_section(request):
    form = Step1InsuranceForm(request.POST)
    return render(
        request,
        "partials/claims_section.html",
        {"form": form, "has_claims": request.POST.get("has_claims")},
    )


def decline_section(request):
    form = Step1InsuranceForm(request.POST)
    return render(
        request,
        "partials/decline_section.html",
        {"form": form, "declined": request.POST.get("declined_before")},
    )
