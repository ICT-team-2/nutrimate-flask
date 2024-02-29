import pandas as pd
import cx_Oracle
import json
from flask_restful import Resource
from sklearn.metrics.pairwise import cosine_similarity
from flask import request

class DietRecommend(Resource):
    def __init__(self):
        self.conn = cx_Oracle.connect(user='ICT', password='ICT1234', dsn='leeserver.ddns.net:3131/xe',
                                      encoding="UTF-8")

    def get(self):
        user_id = request.args.get('user_id', type=int)

        cursor = self.conn.cursor()

        # 사용자의 식단 유형
        cursor.execute("SELECT user_id, user_diet FROM MEMBER WHERE user_id=%s" % user_id)
        user = cursor.fetchone()

        # 사용자의 음식 영양 정보
        cursor.execute("""
            SELECT f.food_cal, f.food_carbo, f.food_protein, f.food_provi
            FROM RECORD r
            JOIN DIETRECORD d ON r.record_id = d.record_id
            JOIN FOOD f ON d.food_id = f.food_id
            WHERE r.user_id = %s
        """ % user[0])
        rows = cursor.fetchall()

        # 데이터프레임으로 변환
        user_food = pd.DataFrame(rows)

        # csv 파일을 로드
        csv_diet = pd.read_csv('data/diet_recommend.csv', encoding='cp949')

        # 사용자가 기록한 음식이 없는 경우
        if user_food.empty:
            if user[1] == 'CUSTOM':
                # 전체 식단 중 랜덤 추천
                self.recommended_diet = csv_diet.sample(n=1).iloc[0]
            else:
                # user_diet가 같은 식단 중 랜덤 추천
                self.recommended_diet = csv_diet[csv_diet['user_diet'] == user[1]].sample(n=1).iloc[0]
            return self.recommend_diet()

        # 사용자의 식단 유형이 CUSTOM인 경우와 나머지(NORMAL,EXERCISE,KITO,VEGAN)를 분리
        if user[1] == "CUSTOM":
            csv_diet = csv_diet
        else:
            csv_diet = csv_diet[csv_diet['user_diet'] == user[1]]

        # 사용자의 음식 영양 정보 평균을 계산
        user_avg = user_food.mean()

        # csv 식단의 영양 정보를 추출
        csv_nutrition = csv_diet[['food_cal', 'food_carbo', 'food_protein', 'food_provi']]

        # 코사인 유사도를 계산
        similarity = cosine_similarity([user_avg], csv_nutrition)

        # 유사도가 가장 높은 식단 인덱스를 찾기
        recommended_index = similarity.argmax()

        # 추천 식단 찾기
        self.recommended_diet = csv_diet.iloc[recommended_index]

        return self.recommend_diet()

    def recommend_diet(self):
        recommended_diet_json = self.recommended_diet.to_json()
        recommended_diet_obj = json.loads(recommended_diet_json)
        print(recommended_diet_obj)
        return recommended_diet_obj