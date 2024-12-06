from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class QuestionForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField()
    tags = forms.CharField()
    # ВОТ ТУТ ТЭГС ТУПО СПЛОШНЯКОМ ХУЯРЯТСЯ ЧЕРЕЗ ЗАПЯТУЮ НАДО ПОТОМ РЕШИТЬ ЧЕ ДЕЛАТЬ
    