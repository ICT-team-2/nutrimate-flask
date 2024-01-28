#구글 혹은 네이버 포탈등에서 비정형 데이타 이미지 스크래핑하기
from telnetlib import EC

import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
import os,time,csv#표준 라이브러리

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def navernews_it():
    try:
        url = f'https://search.naver.com/search.naver?where=news&query=식습관'
        driver_path = f'{os.path.join(os.path.dirname(__file__), "chromedriver.exe")}'
        service = Service(excutable_path=driver_path)
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)

        options.add_argument('headless')
        #일부 버그용
        options.add_argument('--disable--gpu')
        options.add_argument('window-size=1920x1080')
        options.add_argument(
            'User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        # 4.모든 데이타를 로딩하도록 자바스크립트로 스크롤이 안될때까지 스크롤링한다
        # 스크롤 전 높이 구하기
        scroll_height = driver.execute_script('return document.body.scrollHeight')
        print('scroll_height(스크롤 전):',scroll_height)
        while True:
            # 자바스크립트(자동으로)로 아래로 스크롤하기:window.scrollTo(x좌표,y좌표)
            driver.execute_script(f'window.scrollTo(0,{scroll_height})')
            # 컨텐츠가 로드될때까지 다음 코드 진행을 멈춘다
            time.sleep(3)
            # 스크롤후 높이 다시 구하기
            scroll_height_new = driver.execute_script('return document.body.scrollHeight')
            print('scroll_height(스크롤 후):', scroll_height_new)
            if int(scroll_height_new) > 40000:
                break
            #다시 scroll_height를 새로운 높이로 업데이트

            scroll_height=scroll_height_new
            #sp_nws159
            # sp_nws96

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        #res = requests.get(url)
        #soup = BeautifulSoup(res.text, 'html.parser')

        news_content = []
        news_img_list = []
        news_title = []
        news_url = []
        for i in range(1000):
            # 이미지 추출
            navernews_img = soup.select(f'#sp_nws{i} > div > div > div > a > img')
            navernews_link = soup.select_one(f'#sp_nws{i} > div > div > div > a.news_tit')
            if navernews_link and navernews_img:
                for img_tag in navernews_img:
                    if img_tag:
                        if img_tag.get('data-lazysrc'):
                            news_img_list.append(img_tag.get('data-lazysrc'))
                        else:
                            news_img_list.append(img_tag.get('src'))
            elif navernews_link:
                news_img_list.append("")

            # 뉴스 링크 및 제목 추출
            if navernews_link:
                news_url.append(navernews_link.get('href'))
                news_title.append(navernews_link.get('title'))

            # 뉴스 내용 추출
            navernews_content = soup.select_one(f'#sp_nws{i} > div > div > div.news_contents > div > div > a')
            if navernews_content:
                news_content.append(navernews_content.text)
        return list(zip(news_url, news_img_list, news_title, news_content))



    except Exception as e:
        print('에러발생:', e)




if __name__=='__main__':
    news =navernews_it()
    news_dict = []
    print(news)
    for newslink, imglink, title, content in news:
        news_dict.append({'newslink': newslink, 'imglink': imglink, 'title': title, 'content': content})
    with open(f'navernews.csv', 'w', encoding='utf8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['newslink','imglink','title', 'content'])
        writer.writeheader()
        writer.writerows(news_dict)