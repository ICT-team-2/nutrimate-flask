from flask import request, Response
from flask_restful import Resource
import pandas as pd

class GymRecommend(Resource):
    def post(self):
        # csv 파일 읽기
        df = pd.read_csv('data/fulldata_10_42_01_P_체력단련장업.csv', encoding='cp949')

        # 사용자 입력 받기
        place = request.json.get('place')

        # 주소로 검색
        df['소재지전체주소'] = df['소재지전체주소'].fillna('')
        filtered_df = df[df['소재지전체주소'].str.contains(place)]

        # 필요한 컬럼만 선택
        result_df = filtered_df[['소재지전화', '소재지전체주소', '사업장명']]

        # 결과를 json 형태로 변환
        result = result_df.to_json(orient='records')
        print(result)
        return Response(result, mimetype='application/json')