from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserProfileForm, EditUserProfileForm, ConvertImage
from django.core.files.images import ImageFile

def homepage(request):
    context = {}

    if request.method == 'POST':
        form = ConvertImage(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            convert_link = form.convert()

            context['convert_link'] = convert_link
        else:
            messages.error(request, f'Invalid Form')

    form = ConvertImage()
    context['form'] = form

    return render(request, template_name='homepage.html', context=context)

def register(request):
    if request.user.is_authenticated:
        return redirect('main:homepage')

    context = {}

    if request.method == 'POST':
        form = CreateUserProfileForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'New user "{user.username}" created successfully!')
            auth_login(request, user)
            messages.info(request, f'You are logged in as "{user.username}"!')
            return redirect('main:homepage')
        else:
            for msg in form.error_messages:
                messages.error(request, f'{msg}: {form.error_messages[msg]}')

    form = CreateUserProfileForm()
    context['form'] = form

    return render(request, template_name='register.html', context=context)

def login(request):
    if request.user.is_authenticated:
        return redirect('main:homepage')

    context = {}

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                messages.success(request, f'You are now logged in as "{user.username}"!')
                auth_login(request, user)
                return redirect('main:homepage')
            else:
                for msg in form.error_messages:
                    messages.error(request, f'{msg}: {form.error_messages[msg]}')
        else:
            messages.error(request, f'Invalid Form')

    form = AuthenticationForm()
    context['form'] = form

    return render(request, template_name='login.html', context=context)

@login_required
def profile(request):
    context = {}

    if request.method == 'POST':
        form = EditUserProfileForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'User "{request.user.username}" data updated!')
        else:
            messages.error(request, f'Invalid Form')

    form = EditUserProfileForm(instance=request.user)
    context['form'] = form

    return render(request, template_name='profile.html', context=context)

@login_required
def changePassword(request):
    context = {}

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'User "{request.user.username}" password updated!')
        else:
            messages.error(request, f'Invalid Form')

    form = PasswordChangeForm(request.user)
    context['form'] = form

    return render(request, template_name='changePassword.html', context=context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('main:login')