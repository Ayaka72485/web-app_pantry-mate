from django.shortcuts import render,get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Food 
from .models import Food_template
from .forms import FoodForm
from pykakasi import kakasi
from django.contrib import messages

import requests
from django.http import HttpResponseRedirect
from datetime import date, timedelta

import google.generativeai as genai
from PIL import Image, ImageEnhance, ImageFilter
import json
from django.http import HttpResponse


# Create your views here.
#食材表示
class ListFoodView(ListView):
    template_name = 'map/food_list.html'
    model = Food
    ordering = 'best_by_date'

#各食材の詳細表示
class DetailFoodView(DetailView):
    template_name = 'map/food_detail.html'
    model = Food

#食材登録
class CreateFoodView(CreateView):
    template_name = 'map/food_create.html'
    model = Food
    form_class = FoodForm
    success_url = reverse_lazy('list-food')

#食材削除
class DeleteFoodView(DeleteView):
    template_name = 'map/food_delete.html'
    model = Food
    success_url = reverse_lazy('list-food')

#食材修正
class UpdateFoodView(UpdateView):
    template_name = 'map/food_update.html'
    model = Food
    form_class = FoodForm
    success_url = reverse_lazy('list-food')

#肉類表示
def meat_view(request):
    meat_list = Food.objects.filter(category='meat').order_by('best_by_date')
    return render(request, 'map/meat_list.html', {'meat_list': meat_list})

#野菜表示
def vegetable_view(request):
    vegetable_list = Food.objects.filter(category='vegetable').order_by('best_by_date')
    return render(request, 'map/vegetable_list.html', {'vegetable_list': vegetable_list})

#果物表示
def fruit_view(request):
    fruit_list = Food.objects.filter(category='fruit').order_by('best_by_date')
    return render(request, 'map/fruit_list.html', {'fruit_list': fruit_list})

#飲料表示
def drink_view(request):
    drink_list = Food.objects.filter(category='drink').order_by('best_by_date')
    return render(request, 'map/drink_list.html', {'drink_list': drink_list})

#冷凍食品表示
def frozen_food_view(request):
    frozen_food_list = Food.objects.filter(category='frozen_food').order_by('best_by_date')
    return render(request, 'map/frozen_food_list.html', {'frozen_food_list': frozen_food_list})

#麺類表示
def noodle_view(request):
    noodle_list = Food.objects.filter(category='noodle').order_by('best_by_date')
    return render(request, 'map/noodle_list.html', {'noodle_list': noodle_list})

#調味料表示
def seasoning_view(request):
    seasoning_list = Food.objects.filter(category='seasoning').order_by('best_by_date')
    return render(request, 'map/seasoning_list.html', {'seasoning_list': seasoning_list})

#その他食材表示
def other_view(request):
    other_list = Food.objects.filter(category='other').order_by('best_by_date')
    return render(request, 'map/other_list.html', {'other_list': other_list})

#音声修正
def process_voice_input(request):
    kks = kakasi()
    if request.method == 'POST':
        food_name = request.POST.get('food_name')
        counts_str = request.POST.get('counts')
        if not food_name or not counts_str:
            return render(request, 'voice_input_form.html', {'error': '音声入力が取得できませんでした'})
        
        change_food_name = kks.convert(food_name)
        result = ""
        for converted_word in change_food_name:
            result += f"{converted_word['hira']}"
        
        foods = Food.objects.all()
        matching_foods = [food for food in foods if food.change_hiragana() == result]
        
        try:
            counts = int(counts_str)
        except ValueError:
            return render(request, 'voice_input_form.html',{'error': '数が無効です'})

        if counts == 0:
            if matching_foods:
                food = matching_foods[0]
                food.delete()
                return redirect('/map/list/')
            else:
                return render(request, 'food_not_found.html', {'food_name': food_name})  
        elif counts > 0:
            if matching_foods:
                food = matching_foods[0]
                food.number = food.number - counts 
                food.save()
                return redirect('/map/list/')
            else:
                return render(request, 'food_not_found.html', {'food_name': food_name}) 
        else:
            return render(request, 'voice_input_form.html', {'error': '入力が無効です'})
    return render(request, 'voice_input_form.html')

#レシート読み込み (Gemini)
def process_receipt_input(request):
    if request.method == 'POST' and request.FILES['receipt']:
        receipt_image = request.FILES['receipt']
        image = Image.open(receipt_image)
        model = genai.GenerativeModel(model_name = "gemini-1.5-flash")
        prompt = "商品名('name')（ひらがなまたは半角カタカナで書かれているもの）と個数('quantity')（書いていなかったら1個）を商品ごとのJSON形式で表示してください。もし同じ名前の商品があったら、一つにまとめて、個数をその数にしてください。"
        response = model.generate_content([prompt,image])

        parsed_receipt = json.loads((response.text).replace("```json", "").replace("```", "").strip())

        kks = kakasi()
        kks.setMode("J", "H")  # 漢字をひらがなに変換するモード
        conv = kks.getConverter()

        enriched_receipt = []
        for item in parsed_receipt:
            # 商品名をひらがなに変換
            hiragana_name = conv.do(item['name'])

            # ひらがなでテンプレートを検索
            # food_template = Food_template.objects.filter(title=hiragana_name).first()
            # food_template = Food_template.objects.filter(title__icontains=hiragana_name).first()
            food_template = Food_template.objects.filter(title__icontains=hiragana_name).first()

            # 食材テンプレートが見つかった場合、カテゴリーと賞味期限を補完
            #タイトルを一つずつ検証する
            if food_template:
                item['category'] = food_template.category
                item['best_by_date'] = (date.today() + timedelta(days=food_template.day)).isoformat()  # 賞味期限をデフォルトにテンプレートのdayを追加
            else:
                item['category'] = ''
                item['best_by_date'] = (date.today()).isoformat()

            enriched_receipt.append(item)

        form_class = FoodForm

        return render(request, 'receipt_result.html', {'parsed_receipt': parsed_receipt, 'form': form_class})

    return render(request, 'receipt_input_form.html')

#レシート食材登録
def register_food(request):
    if request.method == 'POST':
        # total_items = len(request.POST.getlist('title_1'))  # この例ではアイテム数を取得します
        # total_items = 7
        total_items = sum(1 for key in request.POST if key.startswith('title_'))
        for i in range(1, total_items + 1):
            title = request.POST.get(f'title_{i}')
            category = request.POST.get(f'category_{i}')
            number = request.POST.get(f'number_{i}')
            unit = request.POST.get(f'unit_{i}')
            best_by_date = request.POST.get(f'best_by_date_{i}')
            if title and category and number and unit and best_by_date:
                existing_food = Food.objects.filter(title=title, best_by_date=best_by_date).first()
                # existing_food = Food.objects.filter(title=title).first()
                if existing_food:
                    # 既存データと新規データをまとめる
                    existing_food.number += int(number)
                    existing_food.save()
                else:
                    Food.objects.create(
                        title=title,
                        category=category,
                        number=number,
                        unit=unit,
                        best_by_date=best_by_date
                    )

        return redirect('list-food')  # 成功時のリダイレクト先

    return render(request, 'template_name.html', {'form': FoodForm()})

#賞味期限通知
def send_line_notify(message, token):
   print(f"送信するメッセージ: {message}")
   print(f"使用するトークン: {token}")
   url = "https://notify-api.line.me/api/notify"
   headers = {"Authorization": f"Bearer {token}"}
   data = {"message": message}


   response = requests.post(url, headers=headers, data=data)


   if response.status_code == 200:
       print("通知を送信しました")
   else:
       print(f"通知の送信に失敗しました: {response.status_code}")
       print(f"エラーメッセージ: {response.text}")


def my_view(request):
   # アクセストークンを設定
   token = "xsoprcumx8vI2y0UaTkZBzDlEHMmO39Focb3ciTTKpH"
  
   tomorrow = date.today() + timedelta(days=1)


   # 賞味期限が明日までの食材を取得
   foods = Food.objects.filter(best_by_date=tomorrow)


   # メッセージを作成
   if foods.exists():
       food_titles = ', '.join([food.title for food in foods])
       message = f"注意: 明日が賞味期限: {food_titles} !!!"
   else:
       message = "賞味期限が明日までの食材はありません。"


   # LINEに通知を送信
   send_line_notify(message, token)


   return HttpResponseRedirect('http://127.0.0.1:8000/map/')

#最初の画面
def index(request):
    return render(request, "map/index.html")