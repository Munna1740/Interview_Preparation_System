from django.shortcuts import render
from .models import *

# Create your views here.

def quiz(request):
    quiz = Quiz.objects.all()
    return render(request, "quiz.html", {"quiz":quiz})


def welcome(request):
    return render(request, "startQuiz.html")

