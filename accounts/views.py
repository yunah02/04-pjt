from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST, require_safe

from .forms import (
    CustomAuthenticationForm,
    CustomPasswordChangeForm,
    CustomUserChangeForm,
    CustomUserCreationForm,
)


# F406 login
@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('books:index')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('books:index')
    else:
        form = CustomAuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


# F407 logout
@login_required
@require_POST
def logout(request):
    auth_logout(request)
    return redirect('books:index')


# F408 signup
@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('books:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('books:index')
    else:
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)


# F409 update
@login_required
@require_http_methods(['GET', 'POST'])
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('books:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {'form': form}
    return render(request, 'accounts/update.html', context)


# F410 delete
@login_required
@require_POST
def delete(request):
    request.user.delete()   # 회원 데이터를 먼저 삭제하고
    auth_logout(request)    # 그다음 세션을 정리한다 (순서 중요)
    return redirect('books:index')


# F411 change_password
@login_required
@require_http_methods(['GET', 'POST'])
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # 변경 후에도 로그인 유지
            return redirect('books:index')
    else:
        form = CustomPasswordChangeForm(request.user)
    context = {'form': form}
    return render(request, 'accounts/change_password.html', context)


# F419 profile
@require_safe
def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    return render(request, 'accounts/profile.html', {'person': person})