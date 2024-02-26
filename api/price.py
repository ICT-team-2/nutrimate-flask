from flask_restful import Resource
from flask import request
import pandas as pd

class Price(Resource):
    def get(self):
        price = int(request.args.get('price'))

        # csv 파일 불러오기
        df = pd.read_csv('./data/menu_price.csv', encoding='cp949')

        # 가격 범위 설정
        if price <= 5000:
            result = df[df['AVG_PRC'] <= 5000]
        elif price <= 10000:
            result = df[(df['AVG_PRC'] > 5000) & (df['AVG_PRC'] <= 10000)]
        elif price <= 20000:
            result = df[(df['AVG_PRC'] > 10000) & (df['AVG_PRC'] <= 20000)]
        elif price <= 30000:
            result = df[(df['AVG_PRC'] > 20000) & (df['AVG_PRC'] <= 30000)]
        else:
            result = df[df['AVG_PRC'] > 30000]

        # 결과 출력
        if len(result) == 0:
            return {"message": "해당 가격 범위에 해당하는 메뉴가 없습니다."}
        else:
            # 식단 유형별로 분리
            response = {}
            for diet_type in ['일반', '고단백', '키토', '비건']:
                diet_result = result[result['식단'] == diet_type]
                if len(diet_result) == 0:
                    response[diet_type] = "해당 식단 유형에 해당하는 메뉴가 없습니다."
                else:
                    # 한 메뉴를 랜덤으로 선택
                    row = diet_result.sample(1).iloc[0]
                    menu_info = {
                        '메뉴 이름': row['MENU_NM'],
                        '이미지': row['이미지'],
                        '칼로리': row['칼로리'],
                        '지방': row['지방'],
                        '탄수화물': row['탄수화물'],
                        '단백질': row['단백질']
                    }
                    response[diet_type] = menu_info
            return response