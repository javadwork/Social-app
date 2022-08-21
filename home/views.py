from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from .models import Post


# Create your views here.

class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {'posts': posts})


class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(pk=post_id, slug=post_slug)
        return render(request, 'home/detail.html', {'post': post})


# def home(request):
#     return render(request, 'home/index.html')
