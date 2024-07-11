from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from core.models import  Especialidad, Psicologo, Horarios, Agenda , Persona
from core.forms import PsicologoForm, EspecialidadForm, HorariosForm, AgendaForm
from django.contrib.auth.models import User
from .forms import PsicologoForm, EspecialidadForm, HorariosForm, AgendaForm
from .models import Especialidad, Psicologo, Horarios, Agenda 






def listar_agendas(request):
    agendas = Agenda.objects.all()
    return render(request, 'core/listar_agendas.html', {'agendas':agendas})

def detallar_agenda(request, id):
    agenda = get_object_or_404(Agenda, pk=id)
    return render(request, 'core/detallar_agenda.html', {'agenda':agenda})

def marcar_consulta(request, id, pk):
    agenda = get_object_or_404(Agenda, pk=id)
    persona = get_object_or_404(Persona, pk=pk)
    persona.consulta.add(agenda)
    return render(request, 'core/area_de_persona_final.html', {'persona':persona})
    
    









    ###### Reserva de hora ######
def registrar_especialidad(request):
    if request.method == "POST":
        form = EspecialidadForm(request.POST, request.FILES)
        if form.is_valid():
            especialidad = form.save(commit=False)
            form.save()
            messages.success(request, "Hecho!")
            return redirect('registrar_especialidad')
    else:
        form = EspecialidadForm() 
    
    return render(request,'core/registrar_especialidad.html', {'form': form})





def registrar_psicologo(request):
    if request.method == "POST":
        form = PsicologoForm(request.POST, request.FILES)
        if form.is_valid():
            psicologo = form.save(commit=False)
            form.save()
            messages.success(request, "Hecho!")
            return redirect('registrar_psicologo')
    else:
        form = PsicologoForm()

    return render(request, 'core/registrar_psicologo.html', {'form': form})

def insertar_horarios(request):
    if request.method == 'POST':
        form = HorariosForm(request.POST, request.FILES)
        if form.is_valid():
            horarios = form.save(commit=False)
            form.save()
            messages.success(request, "Hecho!")
            return redirect('insertar_horarios')
    else:
        form = HorariosForm()
    return render(request, 'core/insertar_horarios.html',{'form':form})

def crear_nueva_agenda(request):
    if request.method == "POST":
        form = AgendaForm(request.POST, request.FILES)
        if form.is_valid():
            agenda = form.save(commit=False)
            messages.success(request, "Hecho!")
            form.save()
            return redirect('listar_agendas')
    else:
        form = AgendaForm()
    return render(request, 'core/crear_nueva_agenda.html',{'form':form})

























def adm(request):
    return render(request,'core/administracion.html')

def area_de_persona(request,id):
    persona = get_object_or_404(Persona, id=id)
    return render(request, 'core/area_de_persona.html',{'persona':persona})

def autenticar_persona(request):
    if request.user.is_authenticated:
        # El usuario ya está autenticado, redirige a la página deseada
        id = request.user.id
        persona = get_object_or_404(Persona, pk=id)
        return render(request, 'core/area_de_persona.html', {'persona': persona})
    else:
        # Si no está autenticado, verifica las credenciales y realiza la autenticación
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            id = user.id
            persona = get_object_or_404(Persona, pk=id)
            return render(request, 'core/area_de_persona.html', {'persona': persona})
        else:
            return render(request, 'core/coming_son.html', {})





