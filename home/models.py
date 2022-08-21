from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    body = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    slug = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.slug} - {self.date_update}'

    def get_absolute_url(self):
        return reverse("home:post_detail", args=(self.id, self.slug))
    