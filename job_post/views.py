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


    jp = [Q(shortRequirement__contains=option) for option in skills]  # make a query for getting all the questions for every skill

    query = jp.pop()  # get the first element

    for q in jp:
        query |= q

    jp = JobPost.objects.filter(query)


    context = {
        'jobpost': jp,
        'skills': skills
    }
    return render(request, 'jobpost.html', context)
