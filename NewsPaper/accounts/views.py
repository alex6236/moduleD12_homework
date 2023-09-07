# from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import MailRegisterForm, MailLoginForm, PasswordChangeForm
from django.contrib.auth.models import Group
import logging

logger = logging.getLogger(__name__)

class MailRegisterView(CreateView):
    model = User
    form_class = MailRegisterForm
    template_name = 'account/signup.html'
    # success_url = '/'
    success_url = '/account/login/'
    # success_url = '/users/profile/'
    # registration_url = '/accounts/signup/'

    def form_valid(self, form):
       user = form.save(request) # type: ignore
       group = Group.objects.get_or_create(name='common')[0]
       user.groups.add(group) 
       user.save()
       return super().form_valid(form)

class MailLoginView(FormView):
    model = User
    form_class = MailLoginForm
    template_name = 'account/login.html'
    success_url = '/'
    login_url = '/accounts/login/'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
    
class LogoutView(LoginRequiredMixin, TemplateView):
    template_name = 'account/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
    
class PasswordChangeView(FormView):
    form_class = PasswordChangeForm
    template_name = 'account/password_change.html'
    # success_url = '/accounts/login/'
    success_url = '/'
    # password_change_url = '/accounts/password/change/'



    