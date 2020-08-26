import json

from django.shortcuts import render

from .models import Case
from profile.models import UserProfile
from service.service import get_base_context


def case(request, card_id):
    context = get_base_context(request.user.id)
    context.update({
        'case': Case.objects.get(id=card_id),
        'case_prize': json.loads(Case.objects.get(id=card_id).prizes),
    })
    if request.user.id:
        context.update({
            'user_level': UserProfile.objects.get(id=request.user.id).level
        })

    return render(request, 'case/case.html', context)
