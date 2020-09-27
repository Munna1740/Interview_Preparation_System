import os

from django.apps import apps
from django.shortcuts import render, redirect
from .models import UserResume
from .models import UserInfo
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm

# Create your views here.
def landingPage(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')


@login_required(login_url='login')
def upload_resume(request):
    if request.method == "POST":
        file = request.FILES['resume_upload']
        if not UserResume.objects.filter(user=request.user).exists():
            resume = UserResume(resume=file, user=request.user)
            resume.save()

            user = UserResume.objects.get(user=request.user)
            resume = user.resume.path
            pdfTotext = convert_pdf_to_string(resume)
            pdfTotext = pdfTotext.lower()
            wordList = pdfTotext.split()
            # list of letters
            cvWords = set(wordList)
            filteredSkills = filter(filterWords, cvWords)

            print('The filtered skills are:')
            skillset = ""
            for skills in filteredSkills:
                skillset += skills + ", "
                print(skills)
            print(skillset)
            userinfo = UserInfo(user=request.user, key_skills=skillset.lower())
            userinfo.save()
        else:
            resume = UserResume.objects.get(user=request.user)
            try:
                os.remove(resume.resume.path)
            except:
                print("CV not found")
            resume.resume = file
            resume.save()

            user = UserResume.objects.get(user=request.user)
            resume = user.resume.path
            pdfTotext = convert_pdf_to_string(resume)
            pdfTotext = pdfTotext.lower()
            wordList = pdfTotext.split()
            # list of letters
            cvWords = set(wordList)
            filteredSkills = filter(filterWords, cvWords)

            print('The filtered skills are:')
            skillset = ""
            for skills in filteredSkills:
                skillset += skills + ", "
                print(skills)
            print(skillset)
            userinfo = UserInfo.objects.get(user=request.user)
            userinfo.key_skills = skillset
            userinfo.save()

    return render(request, 'home.html', {'skillset': skillset})


def convert_pdf_to_string(file_path):
    output_string = StringIO()
    with open(file_path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

    return (output_string.getvalue())


def convert_title_to_filename(title):
    filename = title.lower()
    filename = filename.replace(' ', '_')
    return filename


def split_to_title_and_pagenum(table_of_contents_entry):
    title_and_pagenum = table_of_contents_entry.strip()

    title = None
    pagenum = None

    if len(title_and_pagenum) > 0:
        if title_and_pagenum[-1].isdigit():
            i = -2
            while title_and_pagenum[i].isdigit():
                i -= 1

            title = title_and_pagenum[:i].strip()
            pagenum = int(title_and_pagenum[i:].strip())

    return title, pagenum


# function that filters skills
def filterWords(word):
    skill_tags_model = apps.get_model('ques_generator', 'SkillTags')
    skill_tags = skill_tags_model.objects.all().values('tag')
    s_tags = ''
    for tag in skill_tags:
        s_tags = s_tags + tag['tag'] + ' '
    skills = []
    skills = list(s_tags.split(" "))
    if (word in skills):
        return True
    else:
        return False




#user access control
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
    return render(request, 'examples/login.html', context)

def registration(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
    return render(request, 'examples/registration.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

