from aiocqhttp import CQHttp
from requests_html import HTMLSession
import json

import time

bot = CQHttp(access_token='your-gdfhuighuidfg', enable_http_post=False)
session = HTMLSession()
latest_pub_date = 0

cache_life = 60  # cache有效时长（s）
_cache = {
    "cache_time": 0,
    "data": None
}


def get_count(r):
    dataA = r.html.find('#getStatisticsService', first=True).text
    dataA = dataA[36:-11]
    dataA = json.loads(dataA)
    return dataA


def get_messages(r):
    dataB = r.html.find('#getTimelineService', first=True).text
    dataB = dataB[34:-11]
    dataB = json.loads(dataB)
    return dataB


def get_zone(r):
    data = r.html.find("#getAreaStat", first=True).text
    data = data[27:-11]
    data = json.loads(data)
    return data


def get_rumor(r):
    data = r.html.find("#getIndexRumorList", first=True).text
    data = data[33:-11]
    data = json.loads(data)
    return data


def get_session():
    # update cache
    if time.time() - _cache["cache_time"] >= cache_life:
        _cache["data"] = session.get('https://3g.dxy.cn/newh5/view/pneumonia')
        _cache["cache_time"] = time.time()
        print("缓存过期，正在获取数据")
    else:
        print("正在使用缓存")

    return _cache["data"]


@bot.on_message()
async def handle_msg(context):
    if context['message_type'] != 'group':
        return
    if context['message'] == 'test':
        r = get_session()
        data = get_count(r)
        message = f'确诊:{data["confirmedCount"]} 疑似:{data["suspectedCount"]} 治愈:{data["curedCount"]} 死亡:{data["deadCount"]}'
        await bot.send(context, message)
        dataB = get_messages(r)
        latest = dataB[0]
        message = f'''{latest['title']}
{latest['summary']}
{latest['sourceUrl']}'''
        await bot.send(context, message)
        return
    if context['message'] == '信息':
        message = '''以下是疫情信息链接
https://news.ifeng.com/c/special/7tPlDSzDgVk
https://3g.dxy.cn/newh5/view/pneumonia
https://news.163.com/special/epidemic/?spssid=7283291fcdba1d8c2d13ee3da2cfb760&spsw=7&spss=other
https://m.sohu.com/cbd/sp/NCOV2019
http://m.app.caixin.com/m_topic_detail/1473.html'''
        await bot.send(context, message)
        return
    if context['message'] == '地区':
        r = get_session()
        message = ""
        data = get_zone(r)
        for i in data:
            message += f'{i["provinceShortName"]} '
        message += f'\n发送 查询<地区> 来查询对应人数'
        await bot.send(context, message)
        return
    if context['message'][:2] == '查询':
        r = get_session()
        data = get_zone(r)
        for i in data:
            if i["provinceShortName"] == context['message'][2:]:
                message = f'{i["provinceShortName"]} \n确诊:{i["confirmedCount"]} 治愈:{i["curedCount"]} 死亡:{i["deadCount"]} \n以下是城市信息\n'
                for a in i['cities']:
                    message += f'{a["cityName"]} 确诊:{a["confirmedCount"]} 治愈:{a["curedCount"]} 死亡:{a["deadCount"]}\n'
                await bot.send(context, message)
                return
        await bot.send(context, f'暂无数据')
        return
    if context['message'] == '辟谣':
        r = get_session()
        data = get_rumor(r)
        message = ''
        for i in data:
            message += f'{i["title"]}\n{i["mainSummary"]}\n{i["body"]}\n'
        message += "更多信息请到丁香园网站查询"
        await bot.send(context,message)


bot.run(host='127.0.0.1', port=6700)
