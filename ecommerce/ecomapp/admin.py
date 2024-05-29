from django.contrib import admin
from ecomapp.models import Products
class ProductsAdmin(admin.ModelAdmin):
    list_display=['id','name','price','details']
    list_filter=['cat','is_active','price']

admin.site.register(Products,ProductsAdmin)

