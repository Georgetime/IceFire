# -*- coding:utf-8 -*-

from ice import models
import random
from django.db.models import Count


class AssetDashboard(object):
    """
    This class creates the data that the index page needed
    """
    def __init__(self, request):
        self.request = request
        self.asset_list = models.Asset.objects.all()
        self.data = {}

    def serialize_page(self):
        """
        create data
        """
        # self.data['asset_categories'] = self.get_asset_categories()
        self.data['asset_status_list'] = self.get_asset_status_statistics()
        self.data['department_load'] = self.get_department_load()

    def get_department_load(self):
        """
        get every department load rate
        """
        dataset = {
            'names': [],
            'data': {'load': [], 'left': []}  # left is for the load percent
        }

        for obj in models.Department.objects.all():
            load_val = random.randint(1,100)  # this's for simulate the load rate of department server
            dataset['names'].append(obj.name)
            dataset['data']['load'].append(load_val)
            dataset['data']['left'].append(100-load_val)
        return dataset

    def get_asset_status_statistics(self):
        """Asset status classified statistic"""
        queryset = list(self.asset_list.values('status').annotate(value=Count('status')))
        dataset = {
            'names': [],
            'data': []
        }

        for index, item in enumerate(queryset):
            for db_val, display_name in models.Asset.status_choices:
                if db_val == item['status']:
                    queryset[index]['name'] = display_name
                    if db_val == 0:  #online
                        queryset[index]['itemStyle'] = {
                            'normal': {'color': 'yellowgreen'}
                        }
        dataset['names'] = [item['name'] for item in queryset]
        dataset['data'] = queryset
        return dataset

    # def get_asset_categories(self):
    #
    #     dataset = {
    #         'names': [],
    #         'data': []
    #     }
    #     prefetch_data = [
    #         models.Server,
    #         models.NetworkDevice,
    #         models.SecurityDevice,
    #         models.Software,
    #     ]
    #
    #     for key in prefetch_data:
    #         data_list = list(key.objects.values('sub_asset_type')).annotate(total=Count('sub_asset_type')))
    #         for index, category in enumerate(data_list):
    #             for db_val, display_name in key.sub_asset_type_choices:
    #                 if category['sub_asset_type'] == display_name