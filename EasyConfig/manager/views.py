import os
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import status
from .models import Project, Device, Interface
from .services import get_project_name,get_project_devices
from .serializers import InterfaceSerializer

def members(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def show_projects(request):
    get_project_name(request.user)

    proiecte = Project.objects.filter(user = request.user)
    return render(request, 'My_project.html', {'proiecte' : proiecte})

def show_projects_devices(request, project_id):
    get_project_devices(project_id)

    devices = Device.objects.filter(project_id = project_id).prefetch_related('interfaces')
    return render(request, 'Project_page.html',{'devices' : devices})

@api_view(['POST'])
def save_interface_config(request):
    data = request.data
    device_id = data.get('device_id')
    interface_name = data.get('interface_name')
    print("--- DATE PRIMITE DIN FRONTEND ---")
    print(f"Device ID primit: '{device_id}' (Tip: {type(device_id)})")
    print(f"Nume Interfață primit: '{interface_name}'")
    
    # Opțional, printează ce ai în DB pentru acest device ca să compari
    interfete_existente = list(Interface.objects.filter(device_id=device_id).values_list('name', flat=True))
    print(f"Interfețe salvate în DB pentru acest device: {interfete_existente}")
    print("---------------------------------")

    try:
        interface_obj = Interface.objects.get(device_id = device_id, name = interface_name)
    except Interface.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Interfata nu a fost gasita in baza de date!'
        })
    
    serializer = InterfaceSerializer(interface_obj, data = data, partial = True)
    if serializer.is_valid():
        instance = serializer.save()

        instance.is_configured = True
        instance.save()
        print(f"Configurație salvată cu succes pentru {interface_name}!")
        return Response({
            'status': 'success', 
            'message': 'Configurația a fost salvată cu succes!'
        })
    return Response({
        'status': 'error', 
        'message': serializer.errors
    })