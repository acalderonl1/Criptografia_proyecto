# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path(
        'api/credenciales/create',
        views.CredencialesCreateApiView.as_view(),
        name='credenciales-create',
    ),
    path(
        'api/credenciales/list',
        views.CredencialesListApiView.as_view(),
        name='credenciales-list'
    ),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
