import requests
from requests_html import HTMLSession
import json
import time

session = HTMLSession()


def get_date():
    with open("date.txt", 'r') as file:
        return int(file.read())


def set_date(date):
    with open('date.txt', 'w') as file:
        file.write(str(date))


def get_messages(r):
    dataB = r.html.find('#getTimelineService1', first=True).text
    dataB = dataB[35:-11]
    dataB = json.loads(dataB)
    return dataB


def get_broadcast_groups():
    with open("groups.txt", "r") as file:
        return [i for i in file.read().split("\n")]


def broadcast(msg):
    for i in get_broadcast_groups():
        rep = requests.get('http://127.0.0.1:5700/send_group_msg',
                           params={'access_token': 'your-gdfhuighuidfg', 'group_id': i, 'message': msg})
        print(f"{i} {rep.status_code}")
        time.sleep(1)


def run():
    try:
        get_date()
    except Exception:
        set_date(0)
    r = session.get('https://3g.dxy.cn/newh5/view/pneumonia')
    messages = get_messages(r)
    latest = messages[0]
    if latest['pubDate'] != get_date():
        set_date(latest['pubDate'])
        message = f'''{latest['title']}
{latest['summary']}
{latest['sourceUrl']}'''
        broadcast(message)
    print("无需发送消息")


if __name__ == '__main__':
    while True:
        try:
            run()
        except Exception as e:
            print(e)
        time.sleep(60)
