from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import UserRegistrationForm, ProfileForm
from .models import User
from market.models import SellRequest

User = get_user_model()


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def settings_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/settings.html', {'form': form})


@login_required
def user_search(request):
    q = request.GET.get("q", "")
    users = User.objects.all()
    if q:
        users = users.filter(username__icontains=q)
    users = users.exclude(id=request.user.id)
    return render(request, "accounts/user_search.html", {"users": users, "q": q})


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = profile_user.posts.all()
    return render(request, "accounts/profile.html", {
        "profile_user": profile_user,
        "posts": posts,
    })

def profile_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    items = SellRequest.objects.filter(user=user).order_by("-created_at")
    return render(request, "accounts/profile.html", {
        "profile_user": user,
        "items": items,
    })