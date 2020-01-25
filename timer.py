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
    dataB = r.html.find('#getTimelineService', first=True).text
    dataB = dataB[34:-11]
    dataB = json.loads(dataB)
    return dataB


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
        r = requests.get('http://127.0.0.1:5700/send_group_msg',
                         params={'access_token': 'your-gdfhuighuidfg', 'group_id': 263856041, 'message': message},
                         )
        print(r.status_code)
    print("success")


if __name__ == '__main__':
    while True:
        try:
            run()
        except Exception:
            pass
        time.sleep(60)
