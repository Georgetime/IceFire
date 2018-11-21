# -*- coding:utf-8 -*-
from ice.myauth import UserProfile
from ice import models
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('url', 'name', 'email')


class AssetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Asset
        depth = 2
        fields = ('name', 'sn',)
        # fields = ('name', 'sn', 'server', 'networkdevice')


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Server
        exclude = ('')