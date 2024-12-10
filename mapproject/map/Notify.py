import schedule
import time
from .models import Food
from datetime import datetime, date, timedelta
import requests


# 通知を送信する関数
def send_line_notify(message, token):
   url = "https://notify-api.line.me/api/notify"
   headers = {"Authorization": f"Bearer {token}"}
   data = {"message": message}
  
   response = requests.post(url, headers=headers, data=data)
  
   if response.status_code == 200:
       print("通知を送信しました")
   else:
       print(f"通知の送信に失敗しました: {response.status_code}")
       print(f"エラーメッセージ: {response.text}")


# 賞味期限が近い食材を確認して通知を送信する関数
def check_food_and_notify():
   print("スケジュールされた関数が実行されました")
   today = date.today()
   tomorrow = today + timedelta(days=1)


   # 賞味期限が明日の食材を取得
   foods = Food.objects.filter(expiration_date=tomorrow)


   # 通知メッセージの生成
   if foods:
       message = "以下の食材の賞味期限が近づいています:\n"
       for food in foods:
           message += f"- {food.name}（賞味期限: {food.expiration_date})\n"
   else:
       message = "賞味期限の近い食材はありません。"


   # LINE Notifyに通知を送信
   token = "xsoprcumx8vI2y0UaTkZBzDlEHMmO39Focb3ciTTKpH"  # 取得したアクセストークンに置き換えてください
   send_line_notify(message, token)


# スケジュールを設定（毎日午前10:00に実行）
schedule.every().day.at("12:23").do(check_food_and_notify)


# スケジュールを実行するためのループ
while True:
   print(f"現在の時刻: {datetime.now()}")
   schedule.run_pending()
   time.sleep(60)  # 1分ごとにスケジュールを確認
