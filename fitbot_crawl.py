# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
import fitbot_display

urls = {"전신":"https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%EC%A0%84%EC%8B%A0%EC%9A%B4%EB%8F%99",
        "복부":"https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%EB%B3%B5%EB%B6%80%EC%9A%B4%EB%8F%99",
        "허리":"https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%ED%97%88%EB%A6%AC%EC%9A%B4%EB%8F%99",
        "등":"https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%EB%93%B1%EC%9A%B4%EB%8F%99",
        "가슴":"https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%EA%B0%80%EC%8A%B4%EC%9A%B4%EB%8F%99",
        "어깨":"https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%EC%96%B4%EA%B9%A8%EC%9A%B4%EB%8F%99",
        "허벅지":"https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%EC%96%B4%EA%B9%A8%EC%9A%B4%EB%8F%99",
        "종아리":"https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%EC%A2%85%EC%95%84%EB%A6%AC%EC%9A%B4%EB%8F%99",
        "엉덩이":"https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%EC%97%89%EB%8D%A9%EC%9D%B4%EC%9A%B4%EB%8F%99",
        "팔":"https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%ED%8C%94%EC%9A%B4%EB%8F%99",
        "목":"https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%EB%AA%A9%EC%9A%B4%EB%8F%99",
        "손목":"https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%EC%86%90%EB%AA%A9%EC%9A%B4%EB%8F%99",
        "발목":"https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%EB%B0%9C%EB%AA%A9%EC%9A%B4%EB%8F%99",
        "고관절":"https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%EA%B3%A0%EA%B4%80%EC%A0%88%EC%9A%B4%EB%8F%99",
        "무릎":"https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkQ1&query=%EB%AC%B4%EB%A6%8E%EC%9A%B4%EB%8F%99"}

# 크롤링 함수 구현하기
def _crawl_exercise(parts, channel):
    titles = []
    links = []
    thumb_urls = []

    if parts == "전신":
        titles, links, thumb_urls = _crawl_parts(urls[parts])
    elif parts == "복부":
        titles, links, thumb_urls = _crawl_parts(urls[parts])
    elif parts == "허리":
        titles, links, thumb_urls = _crawl_parts(urls[parts])
    elif parts == "등":
        titles, links, thumb_urls = _crawl_parts(urls[parts])
    elif parts == "가슴":
        titles, links, thumb_urls = _crawl_parts(urls[parts])
    elif parts == "어깨":
        titles, links, thumb_urls = _crawl_parts(urls[parts])
    elif parts == "허벅지":
        titles, links, thumb_urls = _crawl_parts(urls[parts])
    elif parts == "종아리":
        titles, links, thumb_urls = _crawl_parts(urls[parts])
    elif parts == "엉덩이":
        titles, links, thumb_urls = _crawl_parts(urls[parts])
    elif parts == "팔":
        titles, links, thumb_urls = _crawl_parts(urls[parts])
    elif parts == "목":
        titles, links, thumb_urls = _crawl_parts(urls[parts])
    elif parts == "손목":
        titles, links, thumb_urls = _crawl_parts(urls[parts])
    elif parts == "발목":
        titles, links, thumb_urls = _crawl_parts(urls[parts])
    elif parts == "고관절":
        titles, links, thumb_urls = _crawl_parts(urls[parts])
    elif parts == "무릎":
        titles, links, thumb_urls = _crawl_parts(urls[parts])
    elif "더보기" in parts:
        part = parts.split(" ")[0]
        print("스플릿" + part)
        titles, links, thumb_urls = _crawl_parts(urls[part])
        fitbot_display._display_more(channel, part, titles, links)
        return

    fitbot_display._display_crawl(channel, parts, titles, links, thumb_urls)

# 운동 크롤링
def _crawl_parts(url):
    source_code = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source_code, "html.parser")

    thumbnail_urls = [url.find("img")["src"] for url in soup.find_all("div", class_="lesson_thumb")]
    links = [link.find("a")["href"] for link in soup.find_all("div", class_="dti_sec")]
    titles = []

    for link in links:
        url = link
        source_code = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(source_code, "html.parser")
        titles.append(soup.find("div", class_="watch_title").find("h3").get_text())

    return [titles, links, thumbnail_urls]