# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from slack.web.classes.blocks import *
from slack.web.classes.elements import *

SLACK_TOKEN = ''
SLACK_SIGNING_SECRET = ''

app = Flask(__name__)
# /listening 으로 슬랙 이벤트를 받습니다.
slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)

# 안내 메시지 출력
def _display_guide(channel):
    guide = "안녕하세요.\n당신의 건강을 책임지는 핏봇 입니다.\n'@<봇이름> 메뉴'와 같이 멘션하여 매뉴얼을 확인해주세요."

    guide_block = SectionBlock(text=guide)
    block = [guide_block]

    slack_web_client.chat_postMessage(
        channel=channel,
        attachments=[{"blocks": extract_json(block)}],
    )


# 매뉴얼 출력
def _display_manual(channel):
    menu = "목적에 따라 아래와 같이 멘션해주세요.\n\n" \
           + "1. 부위별 운동방법: @<봇이름> 운동\n" \
           + "2. 소모 칼로리 계산: @<봇이름> 칼로리\n" \
           + "3. 다이어트 식단: @<봇이름> 식단"

    menu_block = SectionBlock(text=menu)
    block = [menu_block]

    slack_web_client.chat_postMessage(
        channel=channel,
        attachments=[{"blocks": extract_json(block)}],
    )


# 칼로리 출력
def _display_calory(channel):
    img_url = 'https://postfiles.pstatic.net/MjAxOTA3MTJfMTMg/MDAxNTYyODkxNDUwNjQ5.k0Oqa8Oidfv9UySXLmMKeEjDX_ZYuqUOnCkj_CFzEjkg.oMtkknq0R72ckBuzisNLiLdod_tlp-KktGufNBvqR_sg.PNG.dj5427/칼로리.PNG?type=w773'
    link = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=칼로리+계산기&oquery=운동&tqi=UfNIPlprvOsssAslOGKssssst6d-422061"

    link_block = SectionBlock(text=link)
    img_block = ImageBlock(
        image_url=img_url,
        alt_text="이미지 로드 실패"
    )
    block = [img_block, link_block]

    slack_web_client.chat_postMessage(
        channel=channel,
        attachments=[{"blocks": extract_json(block)}],
    )


# 다이어트 식단 링크 출력
def _display_diet(channel):
    url = 'http://www.10000recipe.com/recipe/list.html?q=%EB%8B%A4%EC%9D%B4%EC%96%B4%ED%8A%B8'
    source_code = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source_code, "html.parser")

    img_url = soup.find("div", class_="gnb_top").find("img")["src"]
    link = "http://www.10000recipe.com/recipe/list.html?q=다이어트"

    link_block = SectionBlock(text=link)
    img_block = ImageBlock(
        image_url=img_url,
        alt_text="이미지 로드 실패"
    )
    block = [img_block, link_block]

    slack_web_client.chat_postMessage(
        channel=channel,
        attachments=[{"blocks": extract_json(block)}],
    )


# 운동 매뉴얼 출력
def _display_exercise(channel):
    message = "(전신/복부/허리/등/가슴/어깨/허벅지/종아리/엉덩이/팔/목/손목/발목/고관절/무릎)\n\n" \
              + "위에서 운동법을 알고자 하는 부위를 골라 다음과 같이 멘션해주세요.\n" \
              + "ex) '@<봇이름> 어깨'"

    message_block = SectionBlock(text=message)
    block = [message_block]

    slack_web_client.chat_postMessage(
        channel=channel,
        attachments=[{"blocks": extract_json(block)}],
    )

# 운동 영상 출력
def _display_crawl(channel, parts, titles, links, thumb_urls):
    thumbnail_block = ImageBlock(
        image_url=thumb_urls[0],
        alt_text="이미지 로드 실패"
    )

    link_block = SectionBlock(
        text=titles[0] + "\n" + links[0] + "\n"
    )

    thumbnail_block2 = ImageBlock(
        image_url=thumb_urls[1],
        alt_text="이미지 로드 실패"
    )

    link_block2 = SectionBlock(
        text=titles[1] + "\n" + links[1] + "\n"
    )

    thumbnail_block3 = ImageBlock(
        image_url=thumb_urls[2],
        alt_text="이미지 로드 실패"
    )

    link_block3 = SectionBlock(
        text=titles[2] + "\n" + links[2] + "\n"
    )

    myBlocks = [thumbnail_block, link_block, thumbnail_block2, link_block2, thumbnail_block3, link_block3]
    slack_web_client.chat_postMessage(
        channel=channel,
        text=parts + " 운동 결과입니다.",
        attachments=[{"blocks": extract_json(myBlocks)}],
    )
    slack_web_client.chat_postMessage(
        channel=channel,
        text="\n추가 정보를 원하시면 '@<봇이름> <부위> 운동 더보기'와 같이 멘션해주세요"
    )

# 매뉴얼 안내
def _alert(channel):
    alert = "※ 매뉴얼에 따라 멘션해주세요 ※\n ('@<봇이름> 메뉴' 참고)"

    alert_block = SectionBlock(text=alert)
    block = [alert_block]

    slack_web_client.chat_postMessage(
        channel=channel,
        attachments=[{"blocks": extract_json(block)}],
    )

# 더보기
def _display_more(channel, part, titles, links):
    message = []
    for i in range(3, len(titles)):
        message.append(titles[i] + "\n" + links[i] + "\n")
    message = u'\n'.join(message)

    message_block = SectionBlock(text=message)
    block = [message_block]
    slack_web_client.chat_postMessage(
        channel=channel,
        text = part + " 운동에 대한 추가링크입니다.",
        attachments=[{"blocks": extract_json(block)}],
    )