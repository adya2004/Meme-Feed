from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class post(models.Model):
    title = models.CharField(max_length = 150)
    template_id = models.TextField()
    top_text = models.TextField(blank=True)
    bottom_text = models.TextField(blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete =  models.CASCADE)
    meme = models.URLField(null = False)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail',kwargs = {'pk':self.pk} )