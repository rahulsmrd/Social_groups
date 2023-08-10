from typing import Any, Optional
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.db import IntegrityError
from groups.models import *

# Create your views here.
class Create(LoginRequiredMixin,generic.CreateView):
    fields=("name","description")
    model=Group

class SingleGroup(generic.DetailView):
    model=Group

class ListGroup(generic.ListView):
    model=Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})
    
    def get(self,request, *args, **kwargs):
        group=get_object_or_404(Group,slug=self.kwargs.get('slug'))

        try:
            GroupMembers.objects.create(user=self.request.user,group=group)

        except IntegrityError:
            messages.warning(self.request,("Warning already member"))
        else:
            messages.success(self.request,'You are Now a member')

        return super().get(request, *args, **kwargs)
    
class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})
    
    def get(self,request, *args, **kwargs):
        
        try:
            membership=GroupMembers.objects.filter(user=self.request.user,group__slug=self.kwargs.get('slug')).get()

        except GroupMembers.DoesNotExist:
            messages.warning(self.request,("You are the member of the group"))
        else:
            membership.delete()
            messages.success(self.request,'You left the group')

        return super().get(request, *args, **kwargs)
    