from flask_restful import Resource
from bs4 import BeautifulSoup
import requests
import pandas as pd

class RecipeResource(Resource):
    def diet_recipe(self):
        link = 'https://www.10000recipe.com/ranking/home_new.html'
        res = requests.get(link)
        source = res.text
        soup = BeautifulSoup(source, 'html.parser')

        # 순위
        numbers = soup.select('#contents_area_full > div > ul > li > p > b')
        numbers_new = [number.text for number in numbers]

        # 제목
        titles = soup.select('#contents_area_full > div > ul > li > div > div.common_sp_caption_tit.line2')
        titles_new = [title.text for title in titles]

        # 이미지 주소
        images = soup.select('#contents_area_full > div > ul > li > div > a > img')
        images_new = [img.get('src') for img in images]

        # 레시피 링크
        urls = soup.select('#contents_area_full > div > ul > li > div > a')
        urls_new = ['https://www.10000recipe.com/' + url.get('href') for url in urls]

        recipe_list = list(zip(numbers_new, titles_new, images_new, urls_new))

        df = pd.DataFrame(recipe_list, columns=['Rank', 'Title', 'Image', 'URL'])
        df.to_csv('recipe.csv', index=False, encoding='utf-8-sig')
        return recipe_list

    def get(self):
        try:
            return self.diet_recipe()
        except Exception as e:
            return {'error': str(e)}, 500