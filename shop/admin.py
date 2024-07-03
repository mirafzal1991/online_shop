from django.contrib import admin

from shop.models import Category, Product, Order, Comment,User

# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Comment)
admin.site.register(User)