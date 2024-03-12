from flask import request, jsonify
from flask_restful import Resource
from keras.models import load_model
import numpy as np
from model.oracle_connection import OracleConnection

class PredictDiabetes(Resource):
    def __init__(self):
        self.oracle = OracleConnection()
        self.conn = self.oracle.connect()
        self.cursor = self.conn.cursor()
        self.model = load_model('./my.h5')
    def get(self):
        # 사용자 ID와 나이,혈당,혈압 받기
        user_id = request.args.get('userId')
        age = request.args.get('age', type=int)
        glucose = request.args.get('glucose', type=int)
        blood_pressure = request.args.get('bloodPressure', type=int)

        # BMI 계산 로직
        self.cursor.execute(f"SELECT user_height, user_weight FROM member WHERE user_id = {user_id}")
        user_height, user_weight = self.cursor.fetchone()
        bmi = user_weight / ((user_height * 0.01) ** 2)
        print(bmi)

        # 각 항목별 선택값 받기
        pregnancies_option = request.args.get('pregnancies', type=int)
        skin_thickness_option = request.args.get('skinThickness', type=int)
        insulin_option = request.args.get('insulin', type=int)
        diabetes_pedigree_function_option = request.args.get('diabetesPedigreeFunction', type=int)

        # 선택에 따른 값 설정
        pregnancies = 2 if pregnancies_option == 1 else 0
        skin_thickness = 30 if skin_thickness_option == 1 else 20
        insulin = 150 if insulin_option == 1 else 200
        diabetes_pedigree_function = 2 if diabetes_pedigree_function_option == 1 else 0.5

        # 모델 입력 데이터 구성
        patient_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age]])
        
        # 모델로 예측
        prediction = self.model.predict(patient_data) * 100
        prediction_rounded = np.round(prediction, 1).tolist()

        return jsonify({'prediction': prediction_rounded})