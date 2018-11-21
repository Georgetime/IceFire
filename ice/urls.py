# -*- coding:utf-8 -*-

from django.urls import path, re_path

from . import views

app_name = 'ice'
urlpatterns = [
    path('', views.index, name='index'),
    path('asset_list/', views.asset_list, name='asset_list'),
    path('asset_detail/<int:asset_id>/', views.asset_detail, name='asset_detail')
]