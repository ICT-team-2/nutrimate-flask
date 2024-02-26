from flask_restful import Resource
from flask import request, jsonify
import requests
import json
import jwt

class Allergy(Resource):
    def post(self):
        # 헤더에서 토큰 가져오기
        token = request.headers.get('Authorization').split(' ')[1]

        # 토큰에서 사용자 정보 가져오기
        user_info = jwt.decode(token, options={"verify_signature": False})

        # 사용자 정보에서 알레르기 정보 가져오기
        allergies = user_info['userInfo']['allergyList']

        # 레시피 정보를 저장할 빈 리스트 생성
        total_recipes = []

        # 각 알레르기에 대해 API 요청 보내기
        for allergy in allergies:
            # Edamam API
            url = "https://api.edamam.com/search"

            # API 키와 필요한 매개변수 입력
            params = {
                'app_id': 'd09e074b',
                'app_key': '858d015699e8a3247d21dc9299f999e0',
                'q': 'Korean food',
                'health': allergy.strip()  # 알레르기 정보를 'health' 파라미터로 전달
            }

            # API 요청 보내기
            response = requests.get(url, params=params)

            # 응답이 성공적이라면
            if response.status_code == 200:
                data = json.loads(response.text)
                recipes = data['hits']

                # 레시피 정보를 총 레시피 리스트에 추가
                for recipe in recipes:
                    recipe_info = recipe['recipe']
                    total_recipes.append({
                        '이미지': recipe_info['image'],
                        '음식 이름': recipe_info['label'],
                        '칼로리': recipe_info['calories']/recipe_info['yield'], # 1인분당 칼로리 정보
                        '건강 관련 정보': recipe_info['healthLabels'],
                        '영양소 정보': recipe_info['totalNutrients']
                    })

        # 레시피 정보 반환
        return jsonify(total_recipes)