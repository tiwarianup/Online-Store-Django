from django.contrib import admin

# Register your models here.
from .models import Order

#register the model in the django-admin
admin.site.register(Order)