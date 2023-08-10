from django.db import models
from django.urls import reverse
from django.conf import settings
from groups.models import Group
from django.contrib.auth import get_user_model

User=get_user_model()   #gives the current user
# Create your models here.

class Post(models.Model):
    user=models.ForeignKey(User, related_name="posts",on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now=True)
    message=models.TextField(blank=True)
    message_html=models.TextField(editable=False)
    group=models.ForeignKey(Group, related_name="posts",blank=True,on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.message
    
    def save(self, *args, **kwargs):
        self.message_html = self.message
        super().save(*args, **kwargs)

    def yourgroups(self):
        l=[]
        print('hello')
        for g in Group:
            if self.user in g.user_group:
                l.append(g)
        return g

    def othergroups(self):

        print('kk')
    def get_absolute_url(self):
        return reverse(
            "posts:single",
            kwargs={
                "username": self.user.username,
                "pk": self.pk
            }
        )
    
    class Meta:
        ordering=['-created_at']
        unique_together=['user','message']
