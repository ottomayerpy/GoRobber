from django.shortcuts import render
from service.service import get_base_context


def send_message(request):
    context = get_base_context(request.user.id)
    return render(request, 'support/send_message.html', context)


def support(request):
    context = get_base_context(request.user.id)
    return render(request, 'support/support.html', context)


def privacy(request):
    context = get_base_context(request.user.id)
    return render(request, 'support/privacy.html', context)


def terms(request):
    context = get_base_context(request.user.id)
    return render(request, 'support/terms.html', context)
