from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView
from formtools.wizard.storage import get_storage
from formtools.wizard.views import NamedUrlSessionWizardView, StepsHelper

from apps.life_forms.forms import BaseQuoteForm, FORM_REGISTRY
from apps.life_forms.models import Test

class QuoteWizardView(LoginRequiredMixin, NamedUrlSessionWizardView):
    """Config-driven multi-step form wizard using django-formtools."""

    steps_config = []
    product_type = None

    def dispatch(self, request, *args, **kwargs):
        self.product_type = kwargs.get("product_type")
        self.steps_config = FORM_REGISTRY.get(self.product_type)
        if not self.steps_config:
            raise Http404("Unknown product type")

        # Initialize storage/steps before custom logic (mirrors WizardView.dispatch)
        self.prefix = self.get_prefix(request, *args, **kwargs)
        self.storage = get_storage(
            self.storage_name, self.prefix, request, getattr(self, "file_storage", None)
        )
        self.steps = StepsHelper(self)
        self.form_list = self.get_form_list()

        requested_slug = kwargs.get("step")
        allowed_slug = self.allowed_slug()
        if (
            requested_slug
            and allowed_slug
            and self.step_index(requested_slug, self.steps_config)
            > self.step_index(allowed_slug, self.steps_config)
        ):
            response = redirect(self.get_step_url(allowed_slug))
            self.storage.update_response(response)
            return response

        response = super().dispatch(request, *args, **kwargs)
        self.storage.update_response(response)
        return response

    def get_prefix(self, request, *args, **kwargs):
        base = super().get_prefix(request, *args, **kwargs)
        return f"{base}-{kwargs.get('product_type')}"

    def get_step_url(self, step):
        return reverse(self.url_name, kwargs={"product_type": self.product_type, "step": step})

    def get_form_list(self):
        return {step["slug"]: step["form"] for step in self.steps_config}

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        product_type = self.product_type
        instance = self.get_instance()
        form_cls = self.form_list.get(step)
        if step and form_cls and issubclass(form_cls, BaseQuoteForm):
            kwargs.update(
                {
                    "instance": instance,
                    "initial": {**(instance.details or {})},
                    "product_type": product_type,
                }
            )
        return kwargs

    def get_template_names(self):
        current = self.steps.current
        step_cfg = self.step_config(current)
        return [step_cfg["template"]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        steps_cfg = self.steps_config
        current_slug = self.steps.current
        context.update(
            {
                "steps": steps_cfg,
                "step": self.step_config(current_slug),
                "product_type": self.product_type,
                "instance": self.get_instance(),
                "current_index": self.step_index(current_slug, steps_cfg) + 1,
            }
        )
        if current_slug == "review":
            context["review_data"] = self.review_payload(self.get_instance())
        return context

    def process_step(self, form):
        response = super().process_step(form)
        instance = self.get_instance()
        self.persist_form(form)
        # track current allowed step (prevent skipping)
        next_slug = self.steps.next
        instance.current_step = next_slug or self.steps.current
        instance.status = "draft"
        instance.save(update_fields=["current_step", "status"])
        return response

    def done(self, form_list, **kwargs):
        instance = self.get_instance()
        for form in form_list:
            self.persist_form(form)
        instance.status = "completed"
        instance.current_step = self.steps.current
        instance.save(update_fields=["status", "current_step"])
        return redirect("quote_list")

    # Helpers
    def get_instance(self):
        if not hasattr(self, "_instance"):
            steps = self.steps_config
            first_slug = steps[0]["slug"]
            instance_id = self.request.GET.get("instance_id") or self.storage.extra_data.get("instance_id")

            if instance_id:
                try:
                    self._instance = Test.objects.get(pk=instance_id, user=self.request.user)
                except Test.DoesNotExist:
                    self._instance = None

            if not getattr(self, "_instance", None):
                draft = (
                    Test.objects.filter(user=self.request.user, product_type=self.product_type, status="draft")
                    .order_by("-id")
                    .first()
                )
                if draft:
                    self._instance = draft
                else:
                    completed = (
                        Test.objects.filter(user=self.request.user, product_type=self.product_type, status="completed")
                        .order_by("-id")
                        .first()
                    )
                    if completed:
                        self._instance = completed
                    else:
                        self._instance = Test.objects.create(
                            user=self.request.user,
                            product_type=self.product_type,
                            current_step=first_slug,
                            status="draft",
                        )
            self.storage.extra_data["instance_id"] = self._instance.pk
        return self._instance

    def step_config(self, step_slug):
        for step in self.steps_config:
            if step["slug"] == step_slug:
                return step
        raise Http404("Unknown step")

    def step_index(self, step_slug, steps):
        for index, step in enumerate(steps):
            if step["slug"] == step_slug:
                return index
        return 0

    def allowed_slug(self):
        instance = self.get_instance()
        return instance.current_step or self.steps_config[0]["slug"]

    def get_step_url(self, step):
        base = reverse(self.url_name, kwargs={"product_type": self.product_type, "step": step})
        return f"{base}?instance_id={self.get_instance().pk}"

    def review_payload(self, instance):
        return {
            "quote_num": instance.quote_num,
            "customer_name": instance.customer_name,
            "product_type": instance.product_type,
            "details": instance.details or {},
            "status": instance.status,
        }

    def persist_form(self, form):
        if hasattr(form, "save"):
            form.save(instance=self.get_instance())


class QuoteListView(LoginRequiredMixin, ListView):
    model = Test
    template_name = "quote/list.html"
    context_object_name = "quotes"

    def get_queryset(self):
        return Test.objects.filter(user=self.request.user).order_by("-id")
