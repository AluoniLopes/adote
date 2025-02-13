from django.contrib import admin
from .models import *


admin.site.register(Raca)
admin.site.register(Tag)

@admin.register(Raca)
class RacaAdmin(admin.model):
    
    

admin.site.register(Pet)
