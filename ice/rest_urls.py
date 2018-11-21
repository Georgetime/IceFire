# -*- coding:utf-8 -*-


from rest_framework import routers
from django.urls import path, include
from ice import rest_views, views as asset_views

router = routers.DefaultRouter()
router.register(r'users', rest_views.UserViewSet)
router.register(r'assets', rest_views.AssetViewSet)
router.register(r'servers', rest_views.ServerViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('asset_list/', rest_views.AssetList),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('dashboard_data', asset_views.get_dashboard_data, name='get_dashboard_data'),

]