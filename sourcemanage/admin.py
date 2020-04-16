from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Metr)
admin.site.register(models.Car)
admin.site.register(models.Carord)
admin.site.register(models.Metorder)