from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from .models import *
from . import forms

REDIRECT_VAR = 'next'

@login_required
def novo_pet(request: HttpRequest) -> HttpResponseRedirect:
    TEMPLATE_NAME = 'novo_pet.html'
    
    ctx = dict(
        tags = Tag.objects.all(),
        racas = Raca.objects.all(),
        form = forms.PetForm()
        )
    
    if request.method == "POST":
        form = forms.PetForm(request.POST, request.FILES)

        if form.is_valid():
            pet = form.save(commit=False)
            pet.save_m2m()
            pet.save()
            messages.add_message(request, constants.SUCCESS, "o Pet %s foi cadastrado sucesso!" % pet.nome)
        else:
            errors = form.errors
            messages.error(request, errors.as_ul())
            return render(request, TEMPLATE_NAME, ctx.update({'form': form}))
            # return redirect('novo_pet')
        return HttpResponseRedirect(request.GET.get(REDIRECT_VAR, reverse('seus_pets')))
    elif request.method == 'GET':
        return render(request, TEMPLATE_NAME, ctx)



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
