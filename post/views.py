from typing import Any, Dict
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import *
from django.http import Http404
from braces.views import SelectRelatedMixin
from post.models import *
from post.forms import *
from django.contrib.auth import get_user_model
User=get_user_model()

# Create your views here.

class PostList(SelectRelatedMixin ,ListView):
    model=Post
    select_related=('user','group')

class UserPost(ListView):
    model=Post
    template_name='post/post_list.html'

    def get_queryset(self):
        try:
            self.post_user=User.objects.prefetch_related("posts").get(username__iexact=self.kwargs.get('username'))
            
        except User.DoesNotExist:
            raise Http404
        
        else:
            return self.post_user.posts.all()
        
        
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context=super().get_context_data(**kwargs)
        context['post_user']=self.post_user
        return context


class PostDetail(SelectRelatedMixin,DetailView):
    model=Post
    select_related=('user','group')

    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))
    
class CreatePost(LoginRequiredMixin,SelectRelatedMixin,CreateView):
    
    # form_class=PostForm
    fields=('message','group')
    model=Post
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({"user": self.request.user})
    #     return kwargs

    def form_valid(self, form):
        self.object=form.save(commit=False)
        self.object.user=self.request.user
        self.object.save()
        return super().form_valid(form)
    
class DeletePost(LoginRequiredMixin,DeleteView,SelectRelatedMixin):
    model=Post
    select_related=('user','group')
    success_url=reverse_lazy("posts:all")

    def get_queryset(self) -> QuerySet[Any]:
        queryset=super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)
    
    def delete(self,*args,**kwargs):
        return super().delete(**args,**kwargs)

