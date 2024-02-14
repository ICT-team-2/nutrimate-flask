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

def Pillyze_it():
    try:
        images_new = []
        titles_new = []
        company_new=[]
        stars_new=[]
        effect1_new=[]
        effect2_new=[]
        gender_new=[]
        age_new=[]
        for gender in genders:
            for age in ages:
                url = f'https://www.pillyze.com/ranking/gender-age?gender={gender}&age={age}&productType=ANY'
                driver_path = f'{os.path.join(os.path.dirname(__file__), "chromedriver.exe")}'
                service = Service(excutable_path=driver_path)
                options = webdriver.ChromeOptions()
                options.add_experimental_option("detach", True)
                options.add_argument('headless')
                # 일부 버그용
                options.add_argument('--disable--gpu')
                options.add_argument('window-size=1920x1080')
                options.add_argument(
                    'User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
                options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
                driver = webdriver.Chrome(service=service, options=options)
                driver.get(url)
                local=WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div > div > div > div > div > div')))
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                pillize = soup.find_all(class_='item-card')

                for item in pillize:
                    # 이미지 주소
                    img_url=item.find('img', class_='item-img')['src']
                    images_new.append(item.find('img', class_='item-img')['src'])
                    # 회사
                    company_new.append(item.find('span', class_='txt1').text)
                    # 제목
                    titles_new.append(item.find('span', class_='txt2').text)
                    # 별점
                    stars_new.append(item.find('span', class_='star-point').text)
                    # 효과
                    card_tags = item.find_all(class_='card-tag')
                    gender_new.append(gender)
                    age_new.append(age)
                    if len(card_tags) == 1:
                        effect1_new.append(card_tags[0].text.strip())
                    else:
                        effect1_new.append("")
                    if len(card_tags) == 2:
                        effect2_new.append(card_tags[1].text.strip())
                    else:
                        effect2_new.append("")

        return list(zip(titles_new, company_new, images_new, stars_new, effect1_new,effect2_new,gender_new,age_new))

    except TimeoutException as e:
        print('지정한 요소를 찾을 수 없어요',e)



if __name__ =='__main__':
    genders = ['UNISEX', 'FEMALE','MALE']
    ages=['ANY','AGE_20_UNDER','AGE_30','AGE_40','AGE_50','AGE_60_OVER','AGE_KIDS']
    news = Pillyze_it()
    news_dict=[]

    for title,company,image_link,star_rating,effect1,effect2,gender,age in news:
        news_dict.append({'imglink': image_link, 'company':company,'title': title, 'star': star_rating, 'effect1': effect1, 'effect2':effect2, 'gender':gender,'age':age})
    with open(f'Nutrients.csv', 'w', encoding='utf8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['imglink','company','title', 'star', 'effect1','effect2','gender','age'])
        writer.writeheader()
        writer.writerows(news_dict)