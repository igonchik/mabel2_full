from django.contrib import admin

from mebel2.models import Material, Calculation, Customer, Order, Edge, EdgeWorkCost, MaterialWorkCost

admin.site.register(Material)
admin.site.register(Edge)
admin.site.register(Calculation)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(EdgeWorkCost)
admin.site.register(MaterialWorkCost)