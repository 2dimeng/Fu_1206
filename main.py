from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import random
import urllib.request
import gzip
import json
import os

today = datetime.now()
city = os.environ['CITY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"].split("\n")
template_id = os.environ["TEMPLATE_ID"].split("\n)


def get_weather_data() :
    city_name = city
    url1 = 'http://wthrcdn.etouch.cn/weather_mini?city='+urllib.parse.quote(city_name)
    #网址1只需要输入城市名，网址2需要输入城市代码
    #print(url1)
    weather_data = urllib.request.urlopen(url1).read()
    #读取网页数据
    weather_data = gzip.decompress(weather_data).decode('utf-8')
    #解压网页数据
    weather_dict = json.loads(weather_data)
    #将json数据转换为dict数据
    return weather_dict

def get_weather(weather_data):
    weather_dict = weather_data
#将json数据转换为dict数据
    if weather_dict.get('desc') == 'invilad-citykey':
        print('你输入的城市名有误，或者天气中心未收录你所在城市')
    elif weather_dict.get('desc') =='OK':
        forecast = weather_dict.get('data').get('forecast')
    weather = [weather_dict.get('data').get('city'),
               weather_dict.get('data').get('wendu')+'℃ ',
               weather_dict.get('data').get('ganmao'),
               forecast[0].get('fengxiang'),
               forecast[0].get('fengli'),
               forecast[0].get('high'),
               forecast[0].get('low'),
               forecast[0].get('type'),
               forecast[0].get('date')]
    return weather

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
chengshi, wengdu,ganmao,fengxiang,fengji,gaowen,diwen,tianqi,riqi= get_weather(get_weather_data())
data0 = {"chengshi":{"value":chengshi,"color":get_random_color()},
        "wengdu":{"value":wengdu,"color":get_random_color()},
        "ganmao":{"value":ganmao,"color":get_random_color()},
        "fengxiang":{"value":fengxiang,"color":get_random_color()},
        "fengji":{"value":fengji[9:11],"color":get_random_color()},
        "gaowen":{"value":gaowen,"color":get_random_color()},
        "diwen":{"value":diwen,"color":get_random_color()},
        "tianqi":{"value":tianqi,"color":get_random_color()},
        "riqi":{"value":riqi,"color":get_random_color()},
        "words":{"value":"12点前钉钉打卡","color":get_random_color()}}
data1 = {"tianqi":{"value":tianqi,"color":get_random_color()},
        "wengdu":{"value":wengdu,"color":get_random_color()},
        "gaowen":{"value":gaowen,"color":get_random_color()},
        "diwen":{"value":diwen,"color":get_random_color()},
        "ganmao":{"value":ganmao,"color":get_random_color()},}
wm.send_template(user_id[0], template_id[0], data0)
wm.send_template(user_id[1], template_id[1], data1)
