# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from mebel2.views import *

handler403 = 'mabel_full.errhandlers.error403'
handler404 = 'mabel_full.errhandlers.error403'
handler500 = 'mabel_full.errhandlers.error500'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^help/$', helpf, name='helpf'),
    url(r'^update/$', update_saw, name='update_saw'),
    url(r'^material/$', material, name='material'),
    url(r'^material/(?P<num>\d+)/$', material, name='material'),
    url(r'^calculate/$', calculate, name='calculate'),
    url(r'^get_calc_result/(?P<calc_id>\d+)/$', get_calc_result, name='get_calc_result'),
    url(r'^getstat_tempalte/(?P<calc_id>\d+)/$', getstat_tempalte, name='getstat_tempalte'),
    url(r'^zakaz/$', zakaz, name='zakaz'),
    url(r'^zakaz/(?P<num>\d+)/$', zakaz, name='zakaz'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
