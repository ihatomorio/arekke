from django.contrib import admin
from .models import Product, Book, Account

admin.site.register(Product)
admin.site.register(Book)
admin.site.register(Account)