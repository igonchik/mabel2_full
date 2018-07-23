# -*- coding: utf-8 -*-
from __future__ import division
from django.shortcuts import render, render_to_response
from mebel2.models import models
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template import RequestContext
from django.db.models import Q
from operator import and_
from functools import wraps
from django.views.decorators.cache import patch_cache_control
from django.db import transaction
from mabel_full import config
import base64
from django.db.models import Max, F
import subprocess
from django.core.mail import send_mail
from copy import deepcopy
from django.db.models import Count
from django.db import connection
import json
from mebel2.models import *
from mebel2.v90_contoller import V90Controller
from django.forms import model_to_dict
from django.core.paginator import Paginator


@transaction.atomic
def helpf(request):
    pass


@transaction.atomic
def material(request, num=1):
    material = Material.objects.all()
    count = material.count()
    pages = Paginator(material, 1)
    try:
        material = pages.page(num)
    except:
        material = pages.page(1)
    return render(request, 'material/main.html', {'material': material, 'page': num, 'pages': pages, 'count': count
                                                  })


@transaction.atomic
def zakaz(request, num=0):
    pass


def update_saw(request):
    if request.method == 'POST':
        records = json.loads(request.body.decode('utf-8'))
        possible_val = [0.4, 0.8, 2]
        possible_struct = ['X', 'Y', 'N']
        rows = list()
        for query in records:
            try:
                len_input = float(query['len_input'])
                width_input = float(query['width_input'])
                count_input = int(query['count_input'])
                border_left = float(query['border_left'])
                border_top = float(query['border_top'])
                border_right = float(query['border_right'])
                border_bottom = float(query['border_bottom'])
                struct = query['struct']
                if border_left in possible_val and border_top in possible_val and border_right in possible_val \
                    and border_bottom in possible_val and struct in possible_struct and len_input > 0 \
                        and width_input > 0 and count_input >= 0:
                    rows.append((len_input, width_input, count_input,
                           (border_top, border_right, border_bottom, border_left),
                           struct))
            except:
                pass
        return render(request, 'raspil/column_preorder.html', {})
    else:
        return render(request, 'raspil/row_saw.html', {'border': True})


def getstat_tempalte(request, calc_id):
    calc = Calculation.objects.select_related('material', 'edge').get(pk=calc_id)
    if calc.ready:
        in_list = calc.page_count
        in_len2 = round(calc.kromka_20)
        in_len04 = round(calc.kromka_04)
        in_len08 = round(calc.kromka_08)
        in_lenrez = round(calc.rez_length)
        in_coast = calc.work_cost
        row_count = calc.detail_count
        return render(request, 'raspil/column_stat.html', {'in_list': in_list, 'in_len2': in_len2,
                                                           'row_count': row_count,
                                                           'in_len04': in_len04, 'in_len08': in_len08,
                                                           'in_lenrez': in_lenrez, 'in_coast': in_coast})
    return HttpResponseBadRequest('Not ready')


def get_calc_result(request, calc_id):
    calc = Calculation.objects.get(pk=calc_id)
    if not calc.ready:
        result = V90Controller.get_celery_result_by_task_id(calc.celery_task_id)
        if result.ready():
            if result.result == 0:
                v90 = V90Controller(calc.id)
                page_count = v90.save_pictures()
                calc_data = v90.get_calc_info()
                for (key, value) in calc_data.items():
                    setattr(calc, key, value)
                calc.ready = True
                calc.page_count = page_count
                calc.work_cost = calc.get_work_cost()
                calc.edge_length = calc.get_edge_length()
                update_fields = ['ready', 'page_count', 'work_cost', 'edge_length'] + list(calc_data.keys())
                calc.save(update_fields=update_fields)
                return JsonResponse({'ready': True, 'result': model_to_dict(calc)})
            else:  # some error in command
                calc.ready = True
                calc.save(update_fields=('ready',))
                return JsonResponse({'ready': True, 'result': model_to_dict(calc)})
        else:
            return JsonResponse({'ready': False})
    else:
        return JsonResponse({'ready': True, 'result': model_to_dict(calc)})


def calculate(request):
    if request.method == 'POST':
        records = json.loads(request.body.decode('utf-8'))
        possible_val = [0.4, 0.8, 2]
        possible_struct = ['X', 'Y', 'N']
        rows = list()
        material_uid = None
        material = None
        edge = None
        for query in records:
            if 'len_input' in query:
                try:
                    len_input = float(query['len_input'])
                    width_input = float(query['width_input'])
                    count_input = int(query['count_input'])
                    border_left = float(query['border_left'])
                    border_top = float(query['border_top'])
                    border_right = float(query['border_right'])
                    border_bottom = float(query['border_bottom'])
                    struct = query['struct']
                    if border_left in possible_val and border_top in possible_val and border_right in possible_val \
                        and border_bottom in possible_val and struct in possible_struct and len_input > 0 \
                            and width_input > 0 and count_input >= 0:
                        rows.append((len_input, width_input, count_input,
                                     (border_top, border_right, border_bottom, border_left), struct))
                except:
                    pass
            else:
                material_uid = int(query['material_uid'])
                edge_uid = int(query['edge_uid'])
                material = Material.objects.get(pk=material_uid).get_size_string()
                edge = Edge.objects.get(pk=edge_uid)
        calc = Calculation.objects.create(data=request.body, material=Material.objects.get(pk=material_uid), edge=edge)
        v90 = V90Controller(calc.id)
        v90.create_xls_file(rows, material)
        task_id = v90.set_celery_task_run_commands()
        calc.celery_task_id = task_id
        calc.save(update_fields=('celery_task_id',))
        return render(request, 'raspil/waiting.html', {'calc_id': calc.id})


@transaction.atomic
def index(request):
    material_id = 1
    edge_id = 1

    material = Material.objects.get(id=material_id)
    edge = Edge.objects.get(id=edge_id)
    in_list = 1
    in_len2 = 2
    in_len04 = 4
    in_len08 = 4
    in_lenrez = 90
    in_coast = '6400.80'

    row = (100, 400, 4, (0.4, 0.4, 0.4, 0.4), 'Y')
    rows = list()
    rows.append(row)
    rows.append(row)

    row_count = len(row)
    return render(request, 'raspil/main.html', {'material': material, 'edge': edge,
                                         'in_list': in_list, 'in_count': row_count, 'in_len2': in_len2,
                                         'in_len08': in_len08, 'in_lenrez': in_lenrez,
                                         'in_len04': in_len04, 'in_coast': in_coast, 'row_count': row_count,
                                         'rows': rows})