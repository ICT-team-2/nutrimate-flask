from flask_restful import Resource
from flask import make_response, jsonify
import json,csv
import os
import pandas as pd
import requests


#
class Navernews(Resource):
    def get(self):
        # CSV 파일이 있는 폴더 경로
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_folder_path = os.path.join(script_dir, '..', 'model')
        csv_file_name = 'navernews.csv'

        # CSV 파일의 전체 경로
        csv_file_path = os.path.join(csv_folder_path, csv_file_name)

        try:
            # CSV 파일 읽기
            df = pd.read_csv(csv_file_path)

            # JSON으로 변환
            json_data = df.to_json(orient='records')
            decoded_data = json.loads(json_data)

            # JSON 형식으로 응답
            return jsonify(decoded_data)
        except Exception as e:
            return jsonify({'error': str(e)})


class Exercise(Resource):
    def get(self):
        # CSV 파일이 있는 폴더 경로
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_folder_path = os.path.join(script_dir, '..', 'model')
        csv_file_name = 'exercise.csv'

        # CSV 파일의 전체 경로
        csv_file_path = os.path.join(csv_folder_path, csv_file_name)

        try:
            # CSV 파일 읽기
            df = pd.read_csv(csv_file_path)

            # JSON으로 변환
            json_data = df.to_json(orient='records')
            decoded_data = json.loads(json_data)

            # JSON 형식으로 응답
            return jsonify(decoded_data)
        except Exception as e:
            return jsonify({'error': str(e)})


class Nutrients(Resource):
    def get(self):
        # CSV 파일이 있는 폴더 경로
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_folder_path = os.path.join(script_dir, '..', 'model')
        csv_file_name = 'Nutrients.csv'

        # CSV 파일의 전체 경로
        csv_file_path = os.path.join(csv_folder_path, csv_file_name)

        try:
            # CSV 파일 읽기
            df = pd.read_csv(csv_file_path)

            # JSON으로 변환
            json_data = df.to_json(orient='records')
            decoded_data = json.loads(json_data)

            # JSON 형식으로 응답
            return jsonify(decoded_data)
        except Exception as e:
            return jsonify({'error': str(e)})

