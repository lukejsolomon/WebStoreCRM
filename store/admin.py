from django.contrib import admin

from .models import *



class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "genderCategory", "seasonCategory", 'newItem')

admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Tag)