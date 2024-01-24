# unstructured_data_scrapping - 구글 혹은 네이버 포탈 등에서 비정형 데이타 이미지 스크래핑하기
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import  By
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os,time #표준 라이브러리
# base64 문자열을 이미지로 저장하기위한 import
import base64
import urllib.request

#base64로 인코딩된 이미지의 문자열을 이미지로 저장
def base64_images_save(base64_images,category,dirname,ext):
    for index,base64_src in enumerate(base64_images):
        # base64인코딩 문자열(/9j~->이진 데이타(b'x67x97~')
        base64_data = base64.b64decode(base64_src.split(',')[1])
        filename = os.path.join(dirname,f'{category}{index + 1}.{ext}')
        with open(filename,'wb') as f:
            f.write(base64_data)
def url_images_save(url_images,category,dirname,ext):
    for index,url in enumerate(url_images):
        filename = os.path.join(dirname, f'{category}{index + 1}.{ext}')
        urllib.request.urlretrieve(url,filename)

def scrapping_images(ext,dirname,url,xpath,**kwargs):
    '''
    이미지 스크래핑하는 함수
    :param ext: 스크래핑 이미지 확장자
    :param dirname: 스크래핑한 이미지를 저장할 디렉토리명
    :param url: 스크래핑할 url
    :param xpath: 스크래핑할 모든 이미지 요소의 xpath
    :param kwargs: query키워드로 전달한 검색어
    :return: 스크래핑한 이미지 갯수 반환
    '''
    try:
        pass
        # 1.스크래핑한 이미지를 저장할 디렉토리 생성
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        # 2.WebDriver객체 생성
        driver_path = f'{os.path.join(os.path.dirname(__file__), "chromedriver.exe")}'
        service = Service(executable_path=driver_path)
        options = webdriver.ChromeOptions()
        # 자동종료 막기
        options.add_experimental_option("detach", True)  #드라이버랑 detach하자
        driver = webdriver.Chrome(service=service, options=options)
        # 3.브라우저에 url로드하기
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
            # 스크롤 후 높이 다시 구하기
            scroll_height_new = driver.execute_script('return document.body.scrollHeight')
            print('scroll_height(스크롤 후):', scroll_height_new)
            if scroll_height == scroll_height_new:
                break
            # 다시 scroll_height를 새로운 높이로 업데이트
            scroll_height = scroll_height_new
        # 5.스크롤링이 끝난 후 이미지 스크래핑하기(모든 요소가 로드가 되었으니까)
        images = driver.find_elements(By.XPATH,xpath)#[WebElement,....] WebElement는 img요소
        # print(images[:10])
        # 6.이미지를 파일로 저장하기 위해 스크래핑한 img 요소의 src 속성에 따라 분리
        # 즉 data:image~ 계열 및 https~계열
        base64_images=[]
        url_images=[]
        # 이미지명 네이밍 방식:고양이1.jpg 고양이2.jpg ....
        for image in images:
            # img태그의 src속성에 가져오기(이미지의 url 혹은 base64인코딩 문자열)
            src = image.get_attribute('src')
            if src.startswith('http'):
                url_images.append(src)
            else:
                base64_images.append(src)
        # 7.스크래핑한 이미지의 소스를 파일로 저장
        base64_images_save(base64_images,category,dirname,ext)
        url_images_save(url_images,category,dirname,ext)

    except Exception as e:
        print('에러발생:',e)
    finally:
        return len(images)

if __name__ == '__main__':
    site = int(input('이미지 스크래핑할 사이트는?(1.네이버 2.구글)'))
    category = input('스크래핑할 이미지를 입력하세요?')
    directory = 'naver' if site == 1 else 'google'
    # 네이버 이미지 XPATH://*[@id="main_pack"]/section[2]/div[1]/div/div/div[1]/div/div/div/div/img
    # 구글 이미지 XPATH://*[@id="islrg"]/div[1]/div/a[1]/div[1]/img
    xpath = '//*[@id="main_pack"]/section[2]/div[1]/div/div/div[1]/div/div/div/div/img' if site == 1 else '//*[@id="islrg"]/div[1]/div/a[1]/div[1]/img'
    url = f'https://search.naver.com/search.naver?where=image&query={category}' if site == 1 else f'https://www.google.com/search?q={category}&tbm=isch'
    print(scrapping_images('JPG',directory,url,xpath,query=category),'개의 이미지가 스크래핑 되었습니다',sep='')