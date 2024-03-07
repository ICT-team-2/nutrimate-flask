from flask_restful import Resource
from flask import request, make_response
import base64
import json
import os
import io
import time
from ultralytics import YOLO
import csv
from PIL import Image
import yaml
import pandas as pd  # pandas 임포트


class FoodDetection(Resource):
    
    def __init__(self):
        self.model = YOLO('last.pt')
        self.timestamp = time.strftime("%d%H%M")
        self.csv_filename = f"foodList.csv"
        self.csv_path = os.path.join('./model', self.csv_filename)
        with open('data.yaml', 'r', encoding='utf-8') as f:
            data_yaml = yaml.safe_load(f)
            self.names = data_yaml['names']
    
    def post(self):
        header_written = os.path.exists(self.csv_path)
        
        base64Encoded = request.form['base64Encoded']
        image_b64 = base64.b64decode(base64Encoded)
        image = Image.open(io.BytesIO(image_b64))
        
        results = self.model.predict(image)
        
        foods = []  # 음식명을 저장할 리스트
        
        with open(self.csv_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Food']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if not header_written:
                writer.writeheader()
            
            for result in results:
                boxes = result.boxes.data
                class_ids = result.boxes.cls
                
                for box, class_id in zip(boxes, class_ids):
                    class_id = int(class_id)
                    
                    if class_id in self.names:
                        if class_id < len(self.names):
                            food_name = self.names[class_id]
                            print(food_name)
                            writer.writerow({'Food': food_name})
                            
                            foods.append(food_name)  # 음식명을 리스트에 추가합니다.
                        else:
                            print(f"Unknown class ID: {class_id}")
        
        save_dir = './images'
        os.makedirs(save_dir, exist_ok=True)
        image.save(os.path.join(save_dir, f'{self.timestamp}.jpg'))
        
        # food.csv 파일 경로
        food_csv_path = 'food.csv'
        
        # food.csv 파일을 읽어옵니다.
        food_df = pd.read_csv(food_csv_path)
        
        food_infos = []  # 음식 정보를 저장할 리스트
        
        # foods 리스트에 있는 각 음식에 대해
        for food in foods:
            # food_df에서 음식명이 일치하는 행을 찾습니다.
            food_info = food_df[food_df['FOOD_NAME'] == food]
            
            # 일치하는 행이 있다면
            if len(food_info) > 0:
                # 첫 번째 행만 가져옵니다. (동일한 음식명이 여러 개 있다면 첫 번째만 사용)
                food_info = food_info.iloc[0]
                
                # 음식 정보를 food_infos 리스트에 추가합니다.
                food_infos.append({
                    'foodId': str(food_info['FOOD_ID']),
                    'foodName': food_info['FOOD_NAME'],
                    'foodCal': food_info['FOOD_CAL'],
                    'foodProtein': food_info['FOOD_PROTEIN'],
                    'foodCarvo': food_info['FOOD_CARBO'],
                    'foodProvi': food_info['FOOD_PROVI'],
                })
        
        return make_response(json.dumps({
            'message': 'analyzed and saved ',
            'csv_file_path': self.csv_path,
            'foods': food_infos  # 음식 정보 리스트
        }, ensure_ascii=False))
