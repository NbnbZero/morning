from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/evanston?unitGroup=metric&key=48S3T493X5B7RFVAAE6V7JAHJ&contentType=json"
  res = requests.get(url).json()
  weather = res['days'][0]['conditions']
  high_temp = round(res['days'][0]['tempmax'])
  city = res['resolvedAddress']
  datee = res['days'][0]['datetime']
  low_temp =  round(res['days'][0]['tempmin'])
  return weather, high_temp, city, low_temp, datee

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = ["So let the memories go on and let the days go on.", "It's never goodbye.", "那时你与我在星光上描绘的梦。", "耀眼的那时，那天的我们", "You are the most important person in your life.",
            "无论漆黑夜空中闪亮的星辰，亦或落日余晖时的太阳。", "I'm doing me regardless", "5v5~wei~"]
  return random.choice(words)

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, high_temp, city, low_temp, datee = get_weather()
data = {"city":{"value":city},"weather":{"value":wea},"high_temp":{"value":high_temp},"low_temp":{"value":low_temp},"date":{"value":datee},"days_from_birth":{"value":get_count()},"birthday_left":{"value":get_birthday()}, "words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
