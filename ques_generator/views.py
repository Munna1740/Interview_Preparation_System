from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from .models import *
from django.apps import apps


# Create your views here.
@login_required
def index(request):
    user_info_model = apps.get_model('user', 'UserInfo')
    user_info = user_info_model.objects.get(user=request.user)
    skills = str(user_info.key_skills).replace(',', "")
    skills = skills.split()

    options = ['X1', 'X2', 'X3']
    qs = [Q(tag__contains=option) for option in skills]  # make a query for getting all the questions for every skill

    query = qs.pop()  # get the first element

    for q in qs:
        query |= q

    qs = Questions.objects.filter(query)

    # questions = Questions.objects.filter(tag__contains=skill1[1])
    # for question in qs:
    #     print(question.question + "\n")
    #
    # for skill in skills:
    #     print(skill + "\n")

    context = {
        'questions': qs,
        'skills': skills
    }
    return render(request, 'questions.html', context)
