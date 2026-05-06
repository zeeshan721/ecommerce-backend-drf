from django.contrib import admin
from .models import Cart,CartItem
from .models import Order
from .models import OrderItem


# Register your models here.

admin.site.register(Cart)

@admin.register(CartItem)

class CarItemAdmin(admin.ModelAdmin):
    list_display = ['cart','product','quantity']


admin.site.register(Order)
admin.site.register(OrderItem)    
