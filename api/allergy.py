from flask_restful import Resource
from flask import request, jsonify
import requests
import json
import cx_Oracle


class Allergy(Resource):
    
    def __init__(self):
        self.conn = cx_Oracle.connect(user='ICT', password='ICT1234',
            dsn='db-ict-2.c3w6gsuguk59.ap-southeast-2.rds.amazonaws.com:1521/orcl',
            encoding="UTF-8")
        self.cursor = self.conn.cursor()
    
    def get(self):
        # 사용자 정보에서 알레르기 가져오기
        userId = request.args.get('userId')
        
        self.cursor.execute(f"SELECT user_allergy FROM member WHERE user_id = {userId}")
        allergies = self.cursor.fetchone()[0]
        
        # 레시피 정보를 저장할 빈 리스트 생성
        total_recipes = []
        
        # Edamam API
        url = "https://api.edamam.com/search"
        
        # API 키와 필요한 매개변수 입력
        params = {
            'app_id': 'd09e074b',
            'app_key': '858d015699e8a3247d21dc9299f999e0',
            'q': 'Korean food'
        }
        
        # 알레르기 정보가 있다면 'health' 파라미터로 전달
        if allergies:
            allergies = allergies.split(', ')
            for i, allergy in enumerate(allergies):
                params[f'health{i}'] = allergy.strip()
        
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
                    '음식이름': recipe_info['label'],
                    '칼로리': recipe_info['calories'] / recipe_info['yield'],  # 1인분당 칼로리 정보
                    '건강관련정보': recipe_info['healthLabels'],
                    '영양소정보': recipe_info['totalNutrients']
                })
        
        # 레시피 정보 반환
        return jsonify(total_recipes)
