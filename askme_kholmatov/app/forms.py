from django import forms
from app.models import *

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class QuestionForm(forms.ModelForm):
    title = forms.CharField()
    body = forms.CharField()
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
    # ВОТ ТУТ ТЭГС ТУПО СПЛОШНЯКОМ ЧЕРЕЗ ЗАПЯТУЮ НАДО ПОТОМ РЕШИТЬ ЧЕ ДЕЛАТЬ
    
    class Meta:
        model = Question
        fields = [
            'title',
            'body',
            'tags',
        ]

class AnswerForm(forms.Form):
    body = forms.CharField()

    class Meta:
        model = Answer
        fields = [
            'body'
        ]