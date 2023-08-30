from django.db import models

from user.models import User
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    status = models.CharField(max_length=12, choices=[('open', 'Open'), ('closed', 'Closed'), ('no_responses', 'no Responses')], default='open')
    

    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
        

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
         
        if not self.slug:
            self.slug = slugify(self.name)
        
        if self.slug != slugify(self.name):
           self.slug_history.create(slug_history=self.slug, Topic=self)
        self.slug = slugify(self.name)

        if self.slug_history.filter(slug_history=self.slug).exists():
                self.slug_history.filter(slug_history=self.slug).delete()
        if (Topic.objects.filter(slug=self.slug).exists() and not self.pk) or SlugHistory.objects.filter(slug_history=self.slug).exists():
            self.slug = slugify(self.name) + '-' + str(self.pk)
        # if self slug is not in history, add it


        
        super(Topic, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('topics:topic_detail', kwargs={'slug': self.slug})

class Response(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey(Topic, related_name='responses', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='responses', on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:50]
    

class SlugHistory(models.Model):

    Topic = models.ForeignKey(Topic, related_name='slug_history', on_delete=models.CASCADE)

    slug_history = models.CharField(max_length=100, unique=True, null=True, blank=True)

