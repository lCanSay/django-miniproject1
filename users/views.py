from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from .models import Profile, Follow
from django.contrib.auth.models import User



# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('postapp:listofposts')
    else:
        form = UserCreationForm()
    return render(request, 'users/registration.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('postapp:listofposts')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('postapp:listofposts')
    

@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)

    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)

    user_profile = get_object_or_404(Profile, user__username=username)
    is_own_profile = request.user == user_profile.user

    followers = Follow.objects.filter(following=user_profile.user)
    following = Follow.objects.filter(follower=user_profile.user)
    is_following = followers.filter(follower=request.user).exists()

    if request.method == 'POST' :
        if is_own_profile:
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('profile', username=request.user.username)

        else:
            if 'follow' in request.POST:
                Follow.objects.get_or_create(follower=request.user, following=user_profile.user)
            elif 'unfollow' in request.POST:
                Follow.objects.filter(follower=request.user, following=user_profile.user).delete()
            return redirect('profile', username=username)

    else:
        profile_form = ProfileUpdateForm(instance=user.profile) if is_own_profile else None

    
    return render(request, 'users/profile.html', {
        'profile': user_profile,
        'profile_form': profile_form,
        'is_own_profile': is_own_profile,
        'is_following': is_following,
        'followers_count': followers.count(),
        'following_count': following.count(),
    })

