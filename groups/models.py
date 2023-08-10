from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User=get_user_model()
from django import template
register=template.Library()

# Create your models here.

class Group(models.Model):
    name=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(allow_unicode=True,unique=True)
    description=models.TextField(blank=True)
    description_html=models.TextField(blank=True,editable=False)
    members=models.ManyToManyField(User,through='GroupMembers')

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('groups:single', kwargs={'slug':self.slug})
    
    class Meta():
        ordering=['name']


class GroupMembers(models.Model):
    group=models.ForeignKey(Group, related_name='memberships', on_delete=models.CASCADE)
    user=models.ForeignKey(User, related_name='user_group',on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username
    
    class Meta():
        unique_together =('group', 'user')
