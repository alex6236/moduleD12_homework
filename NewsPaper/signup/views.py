# from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib.auth.models import Group
import logging

logger = logging.getLogger(__name__)

class RegisterView(FormView):
    model = User
    form_class = RegisterForm
    template_name = 'signup/signup_site.html'
    success_url = '/signup/login_site/'

    def form_valid(self, form):
       user = form.save(request=self.request)
       group = Group.objects.get_or_create(name='common')[0]
       user.groups.add(group) 
       user.save()
       return super().form_valid(form)


class LoginView(FormView):
    model = User
    form_class = LoginForm
    template_name = 'signup/login_site.html'
    success_url = '/'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, TemplateView):
    template_name = 'signup/logout_site.html'
    # success_url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
    


