# -*- coding: utf-8 -*-

from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
import fitbot_crawl, fitbot_display

SLACK_TOKEN = ''
SLACK_SIGNING_SECRET = ''

app = Flask(__name__)

# /listening 으로 슬랙 이벤트를 받습니다.
slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)

ids = [] # for 여러 번 출력 방지

# 챗봇이 멘션을 받았을 경우
@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    #print(event_data)

    # 중복 출력 방지
    if event_data in ids:
        return
    else:
        ids.append(event_data)

    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]

    menu = ["운동", "칼로리", "식단"]
    parts = ["전신", "복부", "허리", "등", "가슴", "어깨", "허벅지", "종아리", "엉덩이", "팔", "목", "손목", "발목", "고관절", "무릎"]

    print(text)

    flag = -1
    for i in range(0, len(text)):
        if text[i] == ' ':
            flag = i
            break

    if flag != -1:
        text = text[flag + 1:]

    print(text)
    if text == '<@UKY7N3VSP>':
        fitbot_display._display_guide(channel)
    elif text == '메뉴':
        fitbot_display._display_manual(channel)
    elif text == menu[0]:
        fitbot_display._display_exercise(channel)
    elif text == menu[1]:
        fitbot_display._display_calory(channel)
    elif text == menu[2]:
        fitbot_display._display_diet(channel)
    elif text in parts:
        fitbot_crawl._crawl_exercise(text, channel)
    elif "더보기" in text:
        print("더보기")
        fitbot_crawl._crawl_exercise(text, channel)
    else:
        fitbot_display._alert(channel)

    ids.clear()

# / 로 접속하면 서버가 준비되었다고 알려줍니다.
@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('127.0.0.1', port=4040)
