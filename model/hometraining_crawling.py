import time
from telnetlib import EC

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import  By
from bs4 import BeautifulSoup
import requests
#지정한 시간동안 요소를 못 찾을때 발생하는 예외
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os,csv


def Dietshin_it():
    try:
        images_exe = []
        images_title = []
        exe_category = []
        exe_video = []
        for exercise in range(37, 41):
            for page in range(1, 13):
                url = f'https://www.dietshin.com/community/hometraining_sub_list.asp?bc={exercise}&gotopage={page}'
                driver_path = f'{os.path.join(os.path.dirname(__file__), "chromedriver.exe")}'
                service = Service(excutable_path=driver_path)
                options = webdriver.ChromeOptions()
                options.add_experimental_option("detach", True)

                options.add_argument('headless')
                options.add_argument('--disable-gpu')
                options.add_argument('window-size=1920x1080')
                options.add_argument(
                    'User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
                options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
                driver = webdriver.Chrome(service=service, options=options)
                driver.get(url)
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                for li_chlid in range(1,13):
                    if not soup.select(f'#container > div > div > ul > li:nth-child({li_chlid})'):
                        break
                    exercise_video = soup.select(f'#container > div > div > ul > li:nth-child({li_chlid})')
                    for image in exercise_video:
                        try:
                            img_tag = image.find('img')
                            if img_tag:
                                images_exe.append(img_tag['src'])
                                images_title.append(img_tag['alt'])
                        except TypeError:
                            pass

                    for span in exercise_video:
                        if span.find('span', class_='part'):
                            cate=span.find('span', class_='part').text
                            exe_category.append(cate)
                    elements = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, f'#container > div > div > ul > li:nth-child({li_chlid})')))
                    elements.click()
                    iframe_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '#container > div > div > div > div > iframe'))
                    )
                    exe_video.append(iframe_element.get_attribute('src'))
                    driver.back()



        return list(zip(images_exe, images_title, exe_category,exe_video))

    except TimeoutException as e:
        print('지정한 요소를 찾을 수 없어요',e)



if __name__ == '__main__':
    news = Dietshin_it()
    news_dict = []
    for imglink, title, category, videolink in news:
        news_dict.append({'imglink': imglink, 'title': title, 'category': category, 'videolink': videolink})
    with open(f'exercise.csv', 'w', encoding='utf8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['imglink', 'title', 'category', 'videolink'])
        writer.writeheader()
        writer.writerows(news_dict)
