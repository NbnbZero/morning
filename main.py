from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

start_date = os.environ['START_DATE']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/evanston?unitGroup=metric&key=48S3T493X5B7RFVAAE6V7JAHJ&contentType=json"
  res = requests.get(url).json()
  weather = res['days'][0]['description']
  high_temp = round(res['days'][0]['tempmax'])
  city = res['resolvedAddress']
  cur_date = res['days'][0]['datetime']
  low_temp =  round(res['days'][0]['tempmin'])
  return weather, high_temp, city, low_temp, cur_date

def get_count(cur_date):
  delta = datetime.strptime(cur_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday(cur_date):
  today = datetime.strptime(cur_date, "%Y-%m-%d")
  next = datetime.strptime(str(today.year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = ["So let the memories go on and let the days go on. So let me remember 오늘 같은 밤이면。", "我会随着那耀眼的星辰，找到再次回来的路。It's Never Goodbye.", "那时你与我在星光上描绘的梦，多美好 大家一起哭笑的记忆。", "耀眼的那时，那天的我们。曾炙热的日子，在夜空中点亮的梦。", "You are the most important person in your life. So be yourself. Be beautiful.",
            "无论漆黑夜空中闪亮的星辰，亦或落日余晖时的太阳，都是独一无二的存在。", "I'm doing me regardless and I don't care what you say about it.", "Cause you're my word. 그 어떤 말이 너만큼 많이 빛날까?", "My favorite song 모두 네가 있어。", "This time you can face the rain; Next time you can beat the pain.", "无缘无故地闷闷不乐时，暂且忘记现实来玩吧!",
            "Everyday we get better to be good aenergy! Everyday getting harder be the one synergy!", "Two baddies, two baddies, one Porsche!", "Laugh it up, laugh it up, 네 고민들은 구석에다 던져 놔"]
  return random.choice(words)

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, high_temp, city, low_temp, cur_date = get_weather()
data = {"city":{"value":city},"weather":{"value":wea},"high_temp":{"value":high_temp},"low_temp":{"value":low_temp},"date":{"value":cur_date},"days_from_birth":{"value":get_count(cur_date)},"birthday_left":{"value":get_birthday(cur_date)}, "words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
