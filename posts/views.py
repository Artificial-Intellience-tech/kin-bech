from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from accounts.models import User

@login_required
def home_view(request):
    posts = Post.objects.select_related('user').order_by('-created_at')
    return render(request, 'posts/home.html', {'posts': posts})

@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.all()
    return render(request, 'posts/profile.html', {'profile_user': user, 'posts': posts})

@login_required
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user != request.user:
        # Only the owner can delete
        return redirect('home')
    if request.method == 'POST':
        post.delete()
        return redirect('profile', username=request.user.username)
    return render(request, 'posts/confirm_delete_post.html', {'post': post})