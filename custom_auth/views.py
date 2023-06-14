from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView

from banking.models.account import Account
from custom_auth.forms import RegisterForm
from custom_auth.tokens import account_activation_token


# class CustomRegisterView(CreateView):
#     form_class = RegisterForm
#     success_url = reverse_lazy("login")
#     template_name = "custom_auth/register_page.html"
#

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'custom_auth/register_page.html'
    success_url = reverse_lazy('email_sent')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        user.is_active = False
        user.save()

        # Send activation email
        mail_subject = 'Activate your account'
        message = render_to_string('custom_auth/activate_email.html', {
            'user': user,
            'domain': self.request.META['HTTP_HOST'],
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        send_mail(mail_subject, message, 'your_email_address', [user.email])

        return response


class EmailSentView(TemplateView):
    template_name = 'custom_auth/email_sent.html'


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            # Send info email
            mail_subject = 'Your account is now activated'
            message = render_to_string('custom_auth/account_activated_email.html', {
                'accounts': Account.objects.filter(user=user),
                'user': user,
                'domain': self.request.META['HTTP_HOST'],
            })
            send_mail(mail_subject, message, 'your_email_address', [user.email])

            # return HttpResponse('Thank you for your email confirmation. Now you can log in to your account.')
            return render(request, 'custom_auth/email_confirmation.html', {'message': 'Thank you for your email confirmation. Now you can log in to your account.'})
        else:
            return HttpResponse('Activation link is invalid!')


class CustomLoginView(LoginView):
    template_name = "custom_auth/login_page.html"
    success_url = reverse_lazy("account_list")
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    template_name = "custom_auth/logout_page.html"
    success_url = reverse_lazy("login")


def email_verification(request):
    return render(request, "custom_auth/verification.html", {})
