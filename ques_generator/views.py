from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from .models import *
from django.apps import apps


@login_required
def index(request):
    user_info_model = apps.get_model('user', 'UserInfo')
    user_info = user_info_model.objects.get(user=request.user)
    skills = str(user_info.key_skills).replace(',', "")
    skills = skills.split()


    qs = [Q(tag__contains=option) for option in skills]

    query = qs.pop()

    for q in qs:
        query |= q

    qs = Questions.objects.filter(query)


    context = {
        'questions': qs,
        'skills': skills
    }
    return render(request, 'questions.html', context)
