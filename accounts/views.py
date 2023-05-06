from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomAuthenticationForm
from django.http import JsonResponse

# 로그인 view
def login(request):
    if request.user.is_authenticated:
        return redirect('posts:index')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return JsonResponse({'valid': True})
    else:
        form = CustomAuthenticationForm()
    
    error = form.errors
    context = {
        # 'form': form,
        'valid': False,
        'error': error,
    }
    return JsonResponse(context)


# 로그아웃 view
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('posts:index')


# 회원가입 view
def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:index')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return JsonResponse({'valid': True})
            return redirect('posts:index')
    else:
        form = CustomUserCreationForm()

    error = form.errors
    print(list(error.keys()))
    context = {
        # 'form': form,
        'valid': False,
        'error_field': list(error.keys())[0],
        'error': error,
    }
    return JsonResponse(context)
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


# 프로필 view
def profile(request, username):
    User = get_user_model()
    person = User.objects.get(username=username)
    context = {
        'person': person,
    }
    return render(request, 'accounts/profile.html', context)


# 프로필 수정 view
@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect('posts:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


# 팔로잉 view
@login_required
def follow(request, user_pk):
    User = get_user_model()
    person = User.objects.get(pk=user_pk)

    if person != request.user:
        if request.user in person.followers.all():
            person.followers.remove(request.user)
            is_followed = False
        else:
            person.followers.add(request.user)
            is_followed = True

        context = {
            'is_followed': is_followed,
            'following_count': person.followings.count(),
            'follower_count': person.followers.count(),
        }
        return JsonResponse(context)
            
    return redirect('accounts:profile', person.get_username)
