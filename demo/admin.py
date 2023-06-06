from demo.models import *
from django.contrib import admin


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'count']


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email']


class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'date_joined']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'date', 'status']
    list_filter = ['status', 'date']


admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Order, OrderAdmin)
# admin.site.register(ItemInOrder)
admin.site.register(Application, ApplicationAdmin)
