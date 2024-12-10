from django.contrib import admin
from .models import Food  #Foodモデルを管理画面に反映
from .models import Food_template

# Register your models here.
admin.site.register(Food) #Foodモデルを管理画面に反映
admin.site.register(Food_template) #Food_templateモデルを管理画面に反映
