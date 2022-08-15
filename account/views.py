from django.shortcuts import render, redirect
from django.views import View
from . import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post


# Create your views here.

class UserRegisterView(View):
    class_form = forms.UserRegisterForm
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        # disallow to execute get,post and another methods
        if request.user.is_authenticated:
            messages.error(request, 'you are past logged in', 'warning')
            return redirect('home:home')
        # allow to execute get,post and another methods
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.class_form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.class_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            messages.success(request, 'you have register', 'success')
            return redirect('home:home')

        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    class_form = forms.UserLoginForm
    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'you are past logged in', 'warning')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.class_form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.class_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                messages.info(request, 'you are logged in', 'info')
                return redirect('home:home')
            else:
                messages.error(request, 'username or password is not math', 'danger')

        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you are logged out', 'success')
        return redirect('home:home')


class UserProfiletView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        # it's better to use the user instance to set a filter on access to user posts
        posts = Post.objects.filter(user=user)
        return render(request, 'account/profile.html', {'user': user, 'posts': posts})
