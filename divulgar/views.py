from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.shortcuts import redirect, render
from django.http import HttpRequest
from .models import *


# Create your views here.
@login_required
def novo_pet(request: HttpRequest):
    if request.method == "GET":
        tags = Tag.objects.all()
        racas = Raca.objects.all()
        return render(request, 'novo_pet.html', {'tags': tags,
                                                 'racas': racas
                                                 })
    elif request.method == 'POST':
        foto = request.FILES.get('foto')
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        estado = request.POST.get('estado')
        cidade = request.POST.get('cidade')
        telefone = request.POST.get('telefone')
        tags = request.POST.getlist('tags')
        raca = request.POST.get('raca')

        pet = Pet(
            usuario=request.user,
            foto=foto,
            nome=nome,
            descricao=descricao,
            estado=estado,
            cidade=cidade,
            telefone=telefone,
            raca_id=raca,
                  )
        pet.save()
        pet.tags.add(*tags)

        tags = Tag.objects.all()
        racas = Raca.objects.all()
        messages.add_message(request, constants.SUCCESS, 
                             'Novo pet cadastrado'
                             )
        return render(request, 'novo_pet.html', {'tags': tags,
                                                 'racas': racas
                                                 })


@login_required
def seus_pets(request: HttpRequest):
    if request.method == "GET":
        pets = Pet.objects.filter(usuario=request.user)
        raca = Raca.objects.all()
        return render(request, 'seus_pets.html', {'pets': pets,
                                                  'racas': raca
                                                  })

 
@login_required
def remover_pet(request: HttpRequest, id):
    pet = Pet.objects.get(id=id)
    if not pet.usuario == request.user:
        messages.add_message(request, constants.ERROR, 
                             'Hoje não! deixe o pet do amigiuiho em paz'
                             )
        return redirect('/divulgar/seus_pets')
    pet.delete()
    messages.add_message(request, constants.SUCCESS, 'Removido com sucesso.')
    return redirect('/divulgar/seus_pets')
