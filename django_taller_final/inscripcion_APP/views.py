from .models import Inscripcion
from .models import Institucion
from inscripcion_APP.models import Inscripcion
from inscripcion_APP.models import Institucion
from inscripcion_APP.forms import FormInscripcion
from django.shortcuts import render, redirect
from .serialiazers import InscripcionSerializer
from .serialiazers import InstitucionSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.http import Http404

# Create your views here.

def index(request):
    return render(request, 'index.html')

# CRUD

def listarinscripciones(request):
    ins = Inscripcion.objects.all()
    data = {'inscripcion': ins}
    return render(request, 'listarinscripciones.html', data)

def inscribir(request):
    form = FormInscripcion()
    if request.method == 'POST':
        form = FormInscripcion(request.POST)
        if form.is_valid():
            form.save()
        return index(request)
    data = {'form' : form}
    return render(request, 'inscribir.html', data)

def eliminarInscripcion(request, id):
    ins = Inscripcion.objects.get(id = id)
    ins.delete()
    return redirect('/inscripciones')

def actualizaInscripcion(request, id):
    ins = Inscripcion.objects.get(id = id)
    form = FormInscripcion(instance=ins)
    if request.method == 'POST':
        form = FormInscripcion(request.POST, instance=ins)
        if form.is_valid():
            form.save()
        return index(request)
    data = {'form': form}
    return render(request, 'inscribir.html', data)

# Class Based Views

class ListarInscripcion(APIView):

    def get(self, request):
        ins = Inscripcion.objects.all()
        serial = InscripcionSerializer(ins, many=True)
        return Response(serial.data)

    def post(self, request):
        serial = InscripcionSerializer(data = request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=status.HTTP_201_CREATED)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DetalleInscripcion(APIView):

    def get_object(self, pk):
        try:
            return Inscripcion.objects.get(pk=pk)
        except Inscripcion.DoesNotExist:
            return Http404
        
    def get(self, request, pk):
        ins = self.get_object(pk)
        serial = InscripcionSerializer(ins)
        return Response(serial.data)

    def put(self, request, pk):
        ins = self.get_object(pk)
        serial = InscripcionSerializer(ins, data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        ins = self.get_object(pk)
        ins.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Function Based Views

@api_view(['GET', 'POST'])
def institucion_list(request):
    if request.method == 'GET':
        ins = Institucion.objects.all()
        serial = InstitucionSerializer(ins, many=True)
        return Response(serial.data)
    
    if request.method == 'POST':
        serial = InstitucionSerializer(data = request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=status.HTTP_201_CREATED)
    return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def institucion_detalle(request, pk):
    try:
        ins = Institucion.objects.get(id = pk)
    except Institucion.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serial = InstitucionSerializer(ins)
        return Response(serial.data)

    if request.method == 'PUT':
        serial = InstitucionSerializer(ins, data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'DELETE':
        ins.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Api Rest

def verinscripcionesDb(request):
    inscripcion = Inscripcion.objects.all()
    data = {'inscripciones' : list(inscripcion.values('id', 'nombre', 'telefono', 'fecha', 'institucion', 'hora', 'estado', 'observaciones'))}

    return JsonResponse(data)