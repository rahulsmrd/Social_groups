from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class home(TemplateView):
    template_name='index.html'

class testpage(TemplateView):
    template_name='test.html'

class thankspage(TemplateView):
    template_name='thanks.html'