import copy
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.urls import reverse
from app.models import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from app.forms import LoginForm

QUESTIONS = [
    {
        'title': 'title' + str(i+1),
        'id': i,
        'text': 'text' + str(i+1),
        'tags': ['tag'+str(i*13%5+4), 'tag'+str(i*3%6), 'tag'+str(i*5%4)] 
    } for i in range(30)
]

# Create your views here.
def index(request):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator((Question.objects.get_new()), per_page=6)
    page = paginator.page(page_num)
    return render(
        request, template_name='index.html', 
        context={'questions': page.object_list, 'page_obj': page})

def title(request):
    question_title = request.GET.get('search')
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator((Question.objects.get_with_title(question_title)), per_page=6)
    page = paginator.page(page_num)
    return render(
        request, template_name='title.html', 
        context={'questions': page.object_list, 'page_obj': page, 'title': question_title})

@login_required
def ask(request):
    return render(request, template_name='ask.html')

def signup(request):
    return render(request, template_name='signup.html')

def hot(request):
    hot_questions = copy.deepcopy(QUESTIONS)
    hot_questions.reverse()
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator((Question.objects.get_hot()), per_page=6)
    page = paginator.page(page_num)
    return render(
        request, template_name='hot.html', 
        context={'questions': page.object_list, 'page_obj': page})

def tag(request, question_tag):
    tag_p = Tag.objects.get(tag__exact=question_tag)
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator((Question.objects.get_with_tag(tag_p)), per_page=6)
    page = paginator.page(page_num)
    return render(request, template_name='tag.html', 
                  context={'questions': page.object_list, 'tag': question_tag, "page_obj": page})

def question(request, question_id):
    one_question = Question.objects.get(id__exact=question_id)
    answers_qs = Answer.objects.get_with_question(one_question)
    return render(request, template_name='question.html', context={'item': one_question, 'answers': answers_qs})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(form)
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))
            else:
                err_msg = 'wrong username or password'
                return render(request, template_name='login.html', context={'err_msg': err_msg})
    return render(request, template_name='login.html', context={'err_msg': ''})

def logout(request):
    auth.logout(request)
    return redirect(reverse('index'))

@login_required
def profile(request):
    return render(request, template_name='index.html')