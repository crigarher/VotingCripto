from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Thread(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.author.username}'
class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    anonymous_author = models.CharField(max_length=255, blank=True, null=True) 
   

    def __str__(self):
        return f'{self.thread.title} - {self.anonymous_author}'