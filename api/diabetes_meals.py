import requests
from bs4 import BeautifulSoup
import pandas as pd

def diabetes_meals():
    link = 'http://www.lampcook.com/food/food_plan_list.php'
    res = requests.get(link)
    res.encoding = 'utf-8'
    source = res.text
    soup = BeautifulSoup(source, 'html.parser')

    # 제목
    titles = soup.select('#div_main_content > div > ul > li > div > div:nth-child(2)')
    titles_new = [title.text for title in titles]

    # 이미지 주소
    images = soup.select('#div_main_content > div > ul > li > div > a > img')
    images_new = ['http://www.lampcook.com' + img.get('src') for img in images]

    # 링크
    urls = soup.select('#div_main_content > div > ul > li > div > a')
    urls_new = ['http://www.lampcook.com/food/food_plan_view.php?idx_no=' + str(index + 1) for index, url in enumerate(urls)]

    meal_list = [
        {'Title': titles, 'Image': images, 'URL': urls}
        for titles, images, urls in zip(titles_new, images_new, urls_new)
    ]

    df = pd.DataFrame(meal_list, columns=['Title', 'Image', 'URL'])
    df.to_csv('meal.csv', index=False, encoding='utf-8-sig')
    print(meal_list)
    return meal_list

if __name__ == '__main__':
    diabetes_meals()