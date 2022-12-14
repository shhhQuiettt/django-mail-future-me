from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView
from mailing.models import EmailMessage

from .forms import CreateUserForm, LoginForm
from .permissions import LoginRequiredMixin, LogoutRequiredMixin
from .utils import activate_user, send_confirmation_mail


class LoginView(LoginView):
    redirect_authenticated_user = True
    authentication_form = LoginForm

    def form_valid(self, form):
        if not form.cleaned_data["remember_me"]:
            # Session expires when user closes browser
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super().form_valid(form)


class SignUp(LogoutRequiredMixin, FormView):
    template_name = "registration/signup.html"
    form_class = CreateUserForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        # TODO: How can I obtain user from FormView instead of saving and fetching it again?
        form.save()
        email = form.data.get("email")
        send_confirmation_mail(
            user=get_object_or_404(get_user_model(), email=email),
            domain=self.request.META["HTTP_HOST"],
        )
        messages.add_message(
            self.request, messages.INFO, f"Veryfication email has been sent to {email}"
        )

        return super().form_valid(form)


def activate_account(request, uidb64, token):
    err = activate_user(uidb64=uidb64, token=token)
    print(err)

    message, level = (
        ("Email confirmed! Now you can log in", messages.INFO)
        if err is None
        else (err, messages.ERROR)
    )
    print(message, level)

    messages.add_message(request, level, message)

    return redirect(reverse("login"))


class Profile(LoginRequiredMixin, ListView):
    template_name = "members/profile.html"
    model = EmailMessage
    paginate_by = 3
