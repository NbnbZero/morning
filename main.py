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
test = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

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

def get_words():
  recent_db = []
  words_db = ["This time you can face the rain; Next time you can beat the pain.", "입에 붙어, like a snack, 다시, repeat, 되는 trap 이 리듬, make it pop like soda", "Watch me~ Ooh, 24/7 아직 부족해~ 들리니? 함께 있는 매일, put it on replay", "뱉는 순간 heartbeat, bum, bum, bum! Cool kid 다운 kick on the drum, drum, drum!", "令人愉悦的声音 笑意盈盈；一同唱起的歌声 一起去往那时 愉快的曾经。",
             "Trouble, trouble like a miscode, 비상이 걸려 버-버퍼링이야, I’m on that Glitch Mode", "Scratch that bring it back! 네 앞에선", "以最高的声音呼唤你的名字, 也许你就会听到吧；花朵在最为悲痛的春天盛开的话, 我会觉得那就像你的声音。", "So let me remember 오늘 같은 밤이면", "我会随着那耀眼的星辰, 找到再次回来的路 It's Never Goodbye.", "那时你与我在星光上描绘的梦, 多美好 大家一起哭笑的记忆。",
             "耀眼的那时, 那天的我们；曾炙热的日子, 在夜空中点亮的梦。", "无论漆黑夜空中闪亮的星辰, 亦或落日余晖时的太阳, 都是独一无二的存在。", "I'm doing me regardless and I don't care what you say about it.", "Cause you're my word. 그 어떤 말이 너만큼 많이 빛날까?", "My favorite song 모두 네가 있어。", "无缘无故地闷闷不乐时, 暂且忘记现实来玩吧! 我这就去接你。", "Two baddies, two baddies, one Porsche!",
             "Laugh it up, laugh it up, 네 고민들은 구석에다 던져 놔", "晚安 我的月光 快来投入我的怀抱；躺在夜幕低垂的涟漪上 或许你并不知晓 你的光芒多么绚丽美好。", "Gold dust up my sea 금색 가룰 뿌려 찬란히", "따라와 (Bow down) 지켜봐 (My skill) 놀랄걸 (Say wow) We coming~", "花粉飞扬 烟花再灿烂一些 别让我们陷入傲慢与偏见 享受此刻的自由。", "Feel my rhythm Come with me~ 상상해 봐 뭐든지~", "5v5~~Wei~~~",
             "무한하게 반짝여 넌 Like magic 그 환함에 전부 다 잊어 Bad things", "다함께 손을 잡아요 그리고 하늘을 봐요~ 우리가 함께 만들 세상을 하늘에 그려봐요", "눈이 부시죠 너무나아름답죠~ 마주잡은 두 손으로 우리 모두 함께 만들어 가요", "I'm addicted 끊임없이 말을 걸어주는 나의 aespa! 이런 교감 너의 존잰 날 다른 차원으로 이끌었지", "Ayy, 안 놓칠게, I'm all in 자랑해 하루 종일 다른 건 필요 없어 Nothin' anything. I want you, got it, girl?",
             "더 이상 못 찾겠어 널 유혹해 삼킨 건 Black Mamba!", "Yeppi, you gonna love! Yeppi, you gonna love~ Oh yeppi, yeppi, happy virus 누가 뭐래도 I'm so beautiful", "금세 잔뜩 닿아반짝이잖니 금색 길을 내어 나를 빛내지", "널 만나기 전엔 그저 어두웠지 칠흑 같은 바다 밑을 본 적 있니? 일렁이는 얼굴 표정 없는 매일 괜히 흘러갈 뿐 기대 없던 내일", "突然有一天 银河自我头顶倾泻而下 一边与我问好 眼眸凝视着我 这才察觉到手中的光芒",
             "'She no longer needs me' 널 원할 수록 내 현실은 무거워지고 있어", "그럼에도 나는 더 참지 못해 지금 너에게 달려 가고 싶어 나의 모든 순간이 너를 원하고 있으니", "I'm not going back, back, back, back, back! 다짐했던 난데 우는 널 보면 미쳐 너는 내게 왜, 왜, 왜, 왜, 왜, 왜", "너 이럴 때 마다 또 무너져 난 이제는 다시는 더 이상 더 이상 날 찾지마, no~ no!", "오감이 일렁여 나만이 느낀 exclusive 넌 나의 감성, I love it, my designer",
             "가장 특별한 너를 입을래 매일 I do every night everyday Yeah ayy ayy", "You got what I need, You got what I like 사계절을 함께해도 바래지 않아 내게 변함없는 단 한 사람 그게 너야", "Oh baby it's you 이제 시작이야 무한의 나", "거짓은 들러붙어 끈적해~ 회색 빛 도시 it ain't got a chance", "You should be afraid of us; we're bout to blow up.", "即便你夺走了我的一切, 即便所有人都在阻挡我梦想的脚步, 我也定会全力以赴; 빛이 나는 my way, 빛이 나는 my way",
             "Counting stars, 밤하늘에 펄 Better than your Louis Vuitton, your Louis Vuitton", "I believe in miracles, Energy like that; Something more than physical, So gimme that", "네 맘을 훔칠 black suit 날 향해 빛난 너의 루즈 아찔한 느낌 move it up 손짓 하나로 빠져들게 해", "Touch me, tease me, feel me up; Touch me, tease me, feel me up.",
             "단지 널 사랑해 이렇게 말했지～ 이제껏 준비했던 많은 말을 뒤로한 채", "언제나 니 옆에 있을게~ 이렇게 약속을 하겠어 저 하늘을 바라다보며~",
             "머리 위로 비친 내 하늘 바라다보며~ 널 향한 마음을 이제는 굳혔지만~", "웬일인지 네게 더 다가갈수록~ 우린 같은 하늘 아래 서 있었지~~",
             "就如同漫长的黑夜笼罩着白雪入眠，我会将你的担忧温暖地融化，So I'll be there baby, 在你所有的季节。",
             "Merry-go Merry-go Merry-go-around~ 예쁜 이마 위 입 맞출게요", "五彩缤纷的烟花，专属两个人的精彩旅行，我是你的游乐园。",
             "Yeah I'm gonna, I'm gonna love you~ 숨쉬는 것처럼 I'm gonna love", "이대로 가면 날 사랑했던 널 잊을 수가 있긴 할까?",
             "항상 같은 곳을 봤던 넌 어디에?", "为何我从不知道，这个季节之所以温暖是因为有你在我身边~", "볼 수 있기를 내 안에 어느새 번진 그대란 선물",
             "You're my everything, 그대의 낮과 밤을 지켜 주고 싶어 나 내게 기적이란 너야", "My Graduation 그 첫걸음 많이 행복하게 될 거야~",
             "손 흔들어 안녕 마지막 인사하고 돌아서면 날 기다린 세상으로 가~", "You're my night and day 기다리고 있어 이 거리 널 다시 그리며"]
  return random.choice(words_db)

client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)
wea, high_temp, city, low_temp, cur_date = get_weather()
color = get_random_color()
week_list = ["周一","周二","周三","周四","周五","周六","周日"]
tmp = datetime.strptime(cur_date, "%Y-%m-%d").weekday()
weekday = week_list[tmp]
bless_list = ["叮！这周也要加油吖！", "今天也要健健康康喔！>ε<", "今天也给我好好吃饭！", "今天也会有惊喜嘛！", "好耶！终于到周五！(✿ﾟ▽ﾟ)ノ", "zxr昨天做梦了吗！", "醒醒！醒醒！古德猫宁！~~"]
bless = ""
days_to_next_birth = get_birthday(cur_date)
if days_to_next_birth==0:
  bless = "亲爱的如如生日快乐！>ε<"
else:
  bless = bless_list[tmp]

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
#   "words":{"value":get_words(), "color":get_random_color()},
#   "bless":{"value":bless, "color":get_random_color()}
}
# data = {
#   "song":{"value":city},
#   "sth_to_say":{"value":wea}
# }
res = wm.send_template(user_id, template_id, data)
print(res)
res2 = wm.send_template(lc_id, template_id, data)
print(res2)
