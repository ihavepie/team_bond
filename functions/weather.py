from bs4 import BeautifulSoup
import pymongo
import requests
import cpca

# 此处根据自己的数据库更改
client = pymongo.MongoClient("mongodb://root:password@101.42.53.204:27017/database")
db = client["database"]
col = db["cities_cn"]

# 爬取中国气象网站的信息
def weather_sprider(city):
    try:
        # 根据查询城市在数据库中搜寻,该城市网址
        item = col.find_one({'city': city})
    except TypeError:
        # 若未在数据库中搜寻到, 则返回
        return '气象网站对该地未收录哦~'
    else:
        href = item['href']
        res = requests.get(href)
        res.encoding = 'utf-8'
        bs = BeautifulSoup(res.text, 'html.parser')
        day = bs.find('div', class_='pull-left day actived')
        day_item = day.text.split()
        reply = f"{city}的天气:\n\n" \
                f"天气: {day_item[2]}转{day_item[7]}\n" \
                f"温度: 最高{day_item[5]}到最低{day_item[6]}\n" \
                f"风向: {day_item[3]} - {day_item[8]}\n" \
                f"风速: {day_item[4]} - {day_item[9]}\n\n" \
                f"查询日期: {day_item[1]} ({day_item[0]})"
        return reply

# 通过cpca库, 对语句中的地点进行分割
def weather_quire(text):
    try:
        # 区级地点
        city = cpca.transform_text_with_addrs(text, pos_sensitive=True).loc[0, '区'][:-1]
        return weather_sprider(city)
    except TypeError:
        # 若未找到区级地点, 则搜寻市级地点
        city = cpca.transform_text_with_addrs(text, pos_sensitive=True).loc[0, '市'][:-1]
        return weather_sprider(city)
    except KeyError:
        # 若也未查找到, 则cpca库中可能未收录
        return '输入的地址查询不到哦~'


        

        
