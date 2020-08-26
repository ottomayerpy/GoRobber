import json

from django.template.defaulttags import register
from django.shortcuts import render

from profile.models import UserProfile
from service.models import Payment
from service.service import get_base_context
from case.models import Case


def home(request):
    """ Главная страница """
    context = get_base_context(request.user.id)

    cases = Case.objects.all()
    cases_sum_win = dict()

    #  Считаем максимальную сумму выигрыша который игрок может получить для каждого кейса
    for case in Case.objects.all():
        cases_sum_win.update({
            case: sum(json.loads(case.prizes))
        })

    context.update({
        'cases': cases,
        'cases_sum_win': cases_sum_win
    })

    if request.user.is_authenticated:
        context.update({
            'user_level': UserProfile.objects.get(id=request.user.id).level
        })
    return render(request, 'home/home.html', context)


def rating(request):
    """ Страница "Рейтинг" """
    context = get_base_context(request.user.id)
    context.update({
        'users': UserProfile.objects.order_by('-spent_money')[:20]
    })
    return render(request, 'home/rating.html', context)


def payouts(request):
    """ Страница "Выплаты" """
    context = get_base_context(request.user.id)
    context.update({
        'payment': Payment.objects.filter(name='Вывод')[:20]
    })
    return render(request, 'home/payouts.html', context)


@register.filter
def get_item(dictionary, key):
    """ Фильтр для шаблона. Получить значение словаря по ключу """
    return dictionary.get(key)