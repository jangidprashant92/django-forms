from django.shortcuts import redirect, render

from apps.life_forms.forms import LifeForm


# Create your views here.
def life_form_view(request):
    # demo cache
    step1_data = request.session.get("step1")
    form = LifeForm(request.POST or step1_data or None)

    if request.method == "POST" and form.is_valid():
        request.session["step1"] = form.cleaned_data
        return redirect("step2")

    return render(request, "life_form.html", {"form": form})
