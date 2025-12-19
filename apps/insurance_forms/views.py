from django.shortcuts import render, redirect

from .forms.step2 import Step2PlanForm
from .forms.step1 import Step1InsuranceForm


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
    form = Step1InsuranceForm(request.POST)
    return render(
        request,
        "partials/coverage_options.html",
        {"form": form, "coverage": request.POST.get("coverage")},
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
