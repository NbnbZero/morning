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
lc_id = os.environ["LC_ID"]
template_id = os.environ["TEMPLATE_ID"]
graduation = os.environ["GRADUATION_DATE"]
print(birthday, graduation)

def get_weather():
  url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/evanston?unitGroup=metric&key=48S3T493X5B7RFVAAE6V7JAHJ&contentType=json"
  res = requests.get(url).json()
  weather = res['days'][0]['conditions']
  high_temp = str(round(res['days'][0]['tempmax']))+"°C"
  city = res['resolvedAddress']
  cur_date = res['days'][0]['datetime']
  low_temp =  str(round(res['days'][0]['tempmin']))+"°C"
  return weather, high_temp, city, low_temp, cur_date

def get_count(cur_date):
  delta = datetime.strptime(cur_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_graduation(cur_date):
  delta = datetime.strptime(graduation, "%Y-%m-%d") - datetime.strptime(cur_date, "%Y-%m-%d")
  return delta.days

def get_birthday(cur_date):
  today = datetime.strptime(cur_date, "%Y-%m-%d")
  next = datetime.strptime(str(today.year) + "-" + birthday, "%Y-%m-%d")
  if next < today:
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)
  # return random.choices(range(256), k=3)

def get_words():
  recent_db = []
  words_db = ["This time you can face the rain; Next time you can beat the pain",
              "Watch me~ Ooh, 24/7 아직 부족해~ 들리니?",
              "Scratch that bring it back! 네 앞에선",
              "So let me remember 오늘 같은 밤이면",
              "I'm doing me regardless and I don't care what you say about it",
              "My favorite song 모두 네가 있어",
              "Two baddies, two baddies, one Porsche!",
              "Gold dust up my sea 금색 가룰 뿌려 찬란히",
              "I'm not going back, back, back, back, back",
              "빛이 나는 my way, 빛이 나는 my way",
              "So I'll be there baby, 在你所有的季节",
              "Merry-go Merry-go Merry-go-around",
              "My Graduation 그 첫걸음 많이 행복하게 될 거야",
              "Cause I'm too spicy for your heart",
              "Welcome to MY world",
              "Follow me come and get illusion",
              "Love was all we really need",
              "I'm dancing alone inside my head",
              "This love will never change but I just might go insane",
              "Do you know me now so I can see a smile",
              "Cause I am salty & sweet",
              "Sip sip sipping all night, 더 deep deep deep in all night",
              "이건 마치 hell, yeah I'm unhappy",
              "Til we meet, til we meet again",
              "Baby you and me are a twisted fantasy",
              "We are the cure",
              "말해줘 Merry Merry Christmas",
              "널 만날 거야 이런 날 이해해",
              ]
  return random.choice(words_db)

client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)
wea, high_temp, city, low_temp, cur_date = get_weather()
cur_date = graduation
color = get_random_color()
week_list = ["周一","周二","周三","周四","周五","周六","周日"]
tmp = datetime.strptime(cur_date, "%Y-%m-%d").weekday()
weekday = week_list[tmp]
bless_list = ["叮！这周也要加油吖！", "今天也要健健康康喔！", "今天也给我好好吃饭！", "今天也会有惊喜嘛！", "好耶！终于到周五！", "zxr昨天做梦了吗！", "醒醒！醒醒！古德猫宁！"]
bless = ""
days_to_next_birth = get_birthday(cur_date)
if days_to_next_birth==0:
  bless = "亲爱的如如生日快乐！"
else:
  bless = bless_list[tmp]

words = get_words()

if get_graduation(cur_date)==0:
  words = "My Graduation 그 첫걸음 많이 행복하게 될 거야"
  bless = "亲爱的如如毕业快乐！"

data = {
  "weekday":{"value":weekday, "color":color},
  "city":{"value":city, "color":color},
  "weather":{"value":wea, "color":color},
  "high_temp":{"value":high_temp, "color":color},
  "low_temp":{"value":low_temp, "color":color},
  "date":{"value":cur_date, "color":color},
  "days_to_graduation":{"value":get_graduation(cur_date), "color":color},
  "days_from_birth":{"value":get_count(cur_date), "color":color},
  "birthday_left":{"value":days_to_next_birth, "color":color},
  "words":{"value":words, "color":get_random_color()},
  "bless":{"value":bless, "color":get_random_color()}
}

res = wm.send_template(user_id, template_id, data)
print(res)
res2 = wm.send_template(lc_id, template_id, data)
print(res2)
