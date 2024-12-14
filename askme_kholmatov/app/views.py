import copy
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.urls import reverse
from app.models import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from app.forms import *


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
    err_msg = ''
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            form.save_m2m()  
            return redirect(reverse('question', args=[question.id]))
        else:
            err_msg = 'form error'
            return render(request, template_name='ask.html', context={'err_msg': err_msg, 'form': form})
    else:
        return render(request, template_name='ask.html', context={'err_msg': err_msg, 'form': QuestionForm()})

def signup(request):
    err_msg = ''
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_profile = Profile.objects.create(
                username = new_user
            )
            auth.login(request, new_user)
            new_profile.save()
            return redirect(reverse('index'))
        else:
            render(request, template_name='signup.html', context={'err_msg': err_msg, 'form': form})
    else:
        return render(request, template_name='signup.html', context={'err_msg': err_msg, 'form': SignupForm()})

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
    err_msg = ''
    one_question = Question.objects.get_with_id(question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            new_answer = Answer.objects.create(
                user = request.user,
                question = one_question,
                body = form.cleaned_data['body'],
            )
            new_answer.save()
        else:
            err_msg = 'something wrong with the form'
    answers_qs = Answer.objects.get_with_question(one_question)
    return render(request, template_name='question.html', context={'item': one_question, 'answers': answers_qs, 'err_msg':err_msg})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))
            else:
                return render(request, template_name='login.html', context={'form': form})
        else:
            return render(request, template_name='login.html', context={'form': form})
    return render(request, template_name='login.html', context={'form': LoginForm})

def logout(request):
    auth.logout(request)
    return redirect(reverse('index'))

@login_required
def profile(request):
    return render(request, template_name='index.html')