# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.shortcuts import redirect, render
from django.http import HttpRequest

def cadastro(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('/divulgar/seus_pets/')
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if len(nome.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0 or len(
                confirmar_senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preenche todos os campos')
            return render(request, 'cadastro.html')
        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'Senhas não coincidem')
            return render(request, 'cadastro.html')
        if User.objects.filter(username=nome).exists():
            messages.add_message(request, constants.ERROR, 'Já existe um usuário este nome')
        try:
            user = User.objects.create_user(
                username=nome,
                email=email,
                password=senha,
            )
            messages.add_message(request, constants.SUCCESS, 'Usuário criado com sucesso')
            return redirect('login')
        except:
            messages.add_message(request, constants.ERROR, "Não foi possivel registrar sua conta, tente novamente")
            return render(request, "cadastro.html")

def logar(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('/divulgar/seus_pets/')
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        user = authenticate(username=nome,
                            password=senha)
        if user is not None:
            login(request, user)
            return redirect('/divulgar/seus_pets/')
        else:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos')
            return render(request, 'login.html')


def sair(request: HttpRequest): 
    logout(request)
    messages.add_message(request, constants.SUCCESS, "Desconectado com sucesso!")
    return redirect('/auth/login')
