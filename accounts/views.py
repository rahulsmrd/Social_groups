from django.shortcuts import render
from django.views.generic import CreateView,TemplateView
from django.urls import reverse_lazy
from accounts.models import *
from accounts.forms import *

# Create your views here.

class SignUp(CreateView):
    model=User
    form_class=UserCreateForm
    success_url=reverse_lazy('accounts:login')
    template_name='accounts/signup.html'

class LogIn(TemplateView):
    template_name='accounts/login.html'