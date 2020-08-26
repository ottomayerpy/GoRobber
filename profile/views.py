from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import UserProfile
from service.models import Payment, UserEvent, LevelList
from service.service import get_base_context

from django.contrib import auth
from gorobber.settings import LOGIN_REDIRECT_URL
from django.urls import reverse


def index(request):
    """ Страница профиля """
    if not request.user.is_authenticated:
        return HttpResponse(status=404)
    context = get_base_context(request.user.id)
    context.update({
        'user_event': UserEvent.objects.all().order_by('-id')[:12],
        'user': UserProfile.objects.get(id=request.user.id)
    })

    return render(request, 'profile/profile_base.html', context)


def levels(request):
    """ Страница уровней """
    if not request.user.is_authenticated:
        return HttpResponse(status=404)
    context = get_base_context(request.user.id)
    context.update({
        'user_level': UserProfile.objects.get(id=request.user.id).level,
        'user': UserProfile.objects.get(id=request.user.id),
        'levels': LevelList.objects.all()
    })

    return render(request, 'profile/levels.html', context)


def finance(request):
    """ Страница с историей финансовых операций """
    if not request.user.is_authenticated:
        return HttpResponse(status=404)
    context = get_base_context(request.user.id)
    context.update({
        'payment': Payment.objects.filter(user_id=request.user.id).order_by('-id')[:12],
        'user': UserProfile.objects.get(id=request.user.id)
    })

    return render(request, 'profile/finance.html', context)


def user(request, user_id):
    """ Страница просмотра других пользователей """
    context = get_base_context(request.user.id)
    try:
        context.update({
            'user': UserProfile.objects.get(id=user_id),
            'user_event': UserEvent.objects.filter(user_id=user_id).order_by('-id')[:12],
        })
    except UserProfile.DoesNotExist:
        context.update({
            'user': None
        })
    return render(request, 'profile/user.html', context)


def auth_login(request):
    """ Авторизация пользователя """
    context = get_base_context(request.user.id)
    context.update({
        'form': auth.forms.AuthenticationForm
    })
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse(LOGIN_REDIRECT_URL))
        else:
            context.update({
                'login_error': 'User not exist'
            })
    return render(request, 'profile/login.html', context)
