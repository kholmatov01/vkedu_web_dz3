from django import forms
from app.models import *
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(label='Login')
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Неправильный логин или пароль.")
        return cleaned_data

class QuestionForm(forms.ModelForm):
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea, label='Description')
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
    

    class Meta:
        model = Question
        fields = [
            'title',
            'body',
            'tags',
        ]

class AnswerForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea, label='Answer')

    class Meta:
        model = Answer
        fields = [
            'body'
        ]

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            'name',
            'avatar'
        ]
