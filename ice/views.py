from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from ice.bashboard import AssetDashboard
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from ice import admin, tables, models
import json

# Create your views here.

def index(request):

    return render(request, 'ice/asset.html')


@login_required
def get_dashboard_data(request):
    dashboard_data = AssetDashboard(request)
    dashboard_data.serialize_page()
    return HttpResponse(json.dumps(dashboard_data.data))


@login_required
def asset_list(request):
    # print(request.GET)
    asset_obj_list = tables.table_filter(request, admin.AssetAdmin, models.Asset)
    order_res = tables.get_orderby(request, asset_obj_list, admin.AssetAdmin)
    paginator = Paginator(order_res[0], admin.AssetAdmin.list_per_page)

    page = request.GET.get('page')
    try:
        asset_objs = paginator.page(page)
    except PageNotAnInteger:
        asset_objs = paginator.page(1)
    except EmptyPage:
        asset_objs = paginator.page(paginator.num_pages)

    table_obj = tables.TableHandler(request,
                                    models.Asset,
                                    admin.AssetAdmin,
                                    asset_objs,
                                    order_res
                                    )
    # print(table_obj)
    return render(request, 'ice/asset.html', {'table_obj': table_obj,
                                               'paginator': paginator})


@login_required
def asset_detail(request, asset_id):

    return render(request, 'ice/asset_detail.html')
