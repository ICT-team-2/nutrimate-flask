from flask import request, Response
from flask_restful import Resource
import pandas as pd
import json

class WalkCourse(Resource):
    def get(self):
        # csv 파일 읽기
        df = pd.read_csv('data/KC_CFR_WLK_STRET_INFO_2021.csv')

        # 사용자 입력 받기
        place = request.args.get('place')
        difficulty = request.args.get('difficulty', None)  # 초기값을 None으로 설정
        distance = request.args.get('distance', None)  # 초기값을 None으로 설정
        distance = float(distance) if distance else None

        # 거리 컬럼을 숫자로 변환 (범위의 시작과 끝의 평균 계산)
        df['COURS_LT_CN'] = df['COURS_LT_CN'].apply(
            lambda x: (float(x.split('~')[0].replace('Km미만', '').replace('Km이상', '')) +
                       float(x.split('~')[1].replace('Km미만', '').replace('Km이상', ''))) / 2 if '~' in x else float(x.replace('Km미만', '').replace('Km이상', '')))

        # 사용자가 입력한 값에 따라 데이터 필터링
        if difficulty:
            df = df[df['COURS_LEVEL_NM'] == difficulty]
        if distance:
            df = df[df['COURS_LT_CN'] <= distance]
        filtered_df = df[df['SIGNGU_NM'].str.contains(place)]

        # 필요한 컬럼만 선택
        result_df = filtered_df[['WLK_COURS_FLAG_NM', 'WLK_COURS_NM', 'COURS_DC', 'COURS_LEVEL_NM', 'COURS_LT_CN', 'COURS_TIME_CN', 'LNM_ADDR']]

        # 필터링된 데이터를 JSON 형태로 변환
        result = result_df.to_dict(orient='records')

        # JSON을 문자열로 변환하고, Response 객체에 담아 반환
        return Response(json.dumps(result, ensure_ascii=False), mimetype='application/json')