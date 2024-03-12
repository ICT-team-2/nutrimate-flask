from flask_restful import Resource
import pandas as pd
import os
import random

class HealthMeal(Resource):

    def diabetes_meals(self):
        # csv에서 식단 정보를 가져옴
        df = pd.read_csv(os.path.join(os.path.dirname(__file__), './meal.csv'))
        # DataFrame을 레코드 딕셔너리로 변환
        meals_list = df.to_dict(orient='records')
        # 리스트에서 랜덤으로 3개의 식단을 선택
        random_meals = random.sample(meals_list, 3)
        return {'meals': random_meals}

    def get(self):
        try:
            return self.diabetes_meals()
        except Exception as e:
            return {'error': str(e)}, 500