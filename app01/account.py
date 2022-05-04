from django.shortcuts import render
from django import forms
from app01.utils.bootstrap import BootStrapForm

class LoginForm(BootStrapForm):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput,
        required=True,
    )

    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput,
        required=True,
    )



def login(request):
    if request.method == 'GET':
        form = LoginForm
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        pass

    return render(request, 'login.html', {'form': form})
