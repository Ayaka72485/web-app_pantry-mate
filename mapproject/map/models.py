from django.db import models
from datetime import date
from pykakasi import kakasi

# Create your models here.
CATEGORY = (('meat','肉'),('vegetable','野菜'),('fruit','果物'),('drink','飲料'),('frozen_food','冷凍食品'),('noodle','麺'),('seasoning','調味料'),('other','その他'))
UNIT = (('pieces','個'),('grams','g'),('milliliter','ml'))
class Food(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices = CATEGORY)
    number = models.IntegerField(default = 0)
    unit = models.CharField(max_length=100, choices = UNIT, default='pieces')
    best_by_date = models.DateField(default=date.today)

    def __str__(self): #タイトルを表示
        return self.title

    def change_hiragana(self):
        kks = kakasi()
        change_title = kks.convert(self.title)
        result = ""
        for converted_word in change_title:
            result += f"{converted_word['hira']}"
        return result
    

class Food_template(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices = CATEGORY)
    day = models.IntegerField(default = 0)

    def __str__(self): #タイトルを表示
        return self.title