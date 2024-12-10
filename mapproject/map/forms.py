from django import forms
from .models import Food


class FoodForm(forms.ModelForm):


    class Meta:
        model = Food
        fields = ['title', 'category', 'number', 'unit', 'best_by_date']
        labels = {
            'title': '食材名',
            'category': 'カテゴリー',
            'number': '個数',
            'unit': '単位',
            'best_by_date': '賞味期限',
        }
    
