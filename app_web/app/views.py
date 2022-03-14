# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView)
from .serializers import CredencialesSerializer
from .models import Credenciales
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from braces.views import CsrfExemptMixin
from .AES import aes, utils


"""Servicios Api"""

class CredencialesCreateApiView(CsrfExemptMixin, CreateAPIView):
    authentication_classes = []
    #serializer_class = CredencialesSerializer
    
    def post(self, request, format=None):            
        usuario2 = 'perro'
        serializer = CredencialesSerializer(data=request.data)
    
        if serializer.is_valid(self):            
            clave_en_bytes = bytes(b'\xa4\x19`\r\xf3r\x98 H<\x7f\x9dq\x85\xbc\xf2')            
            usuario_cifrado = aes.cifrar(clave_en_bytes, request.data['usuario'])
            contrasena_cifrada = aes.cifrar(clave_en_bytes, request.data['contrasena'])
            serializer.validated_data['usuario'] = usuario_cifrado
            serializer.validated_data['contrasena'] = contrasena_cifrada
            
            serializer.save()
            return HttpResponse(serializer.data)
        return HttpResponse(serializer.errors)


class CredencialesListApiView(CsrfExemptMixin, ListAPIView):
    authentication_classes = []
    serializer_class = CredencialesSerializer

    def get_queryset(self):
        return Credenciales.objects.all()


"""Servicios Web"""

@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'compras_list.html' )
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))
