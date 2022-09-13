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
  temp = math.floor(res['days'][0]['temp'])
  city = res['resolvedAddress']
  body_temp =  math.floor(res['days'][0]['feelslike'])
  return weather, temp, city, body_temp

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, city, body_temp = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"days_from_birth":{"value":get_count()},"birthday_left":{"value":get_birthday()}}
res = wm.send_template(user_id, template_id, data)
print(res)
