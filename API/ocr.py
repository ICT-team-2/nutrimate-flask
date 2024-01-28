'''
1.필요한 라이브러리 설치
pip install google-cloud-vision google-auth  google-auth-oauthlib
pip install --upgrade google-auth
'''
from flask_restful import Resource,reqparse
from flask import make_response, jsonify
import base64
from google.cloud import vision
from google.oauth2 import service_account
from flask import request
import os
import re
import json
class OCR(Resource):
    def __init__(self):
        self.credentials_path= os.environ['GOOGLE_APPLICATION_CREDENTIALS']#프로젝트 ID,Private Key정보가 있는 .json파일의 경로
    def authenticate_service_account(self):
        # 서비스 계정 키를 로드하여 구글 클라우드 Vision API에 인증하는 함수
        credentials = service_account.Credentials.from_service_account_file(self.credentials_path)
        scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
        return scoped_credentials
    def detect_labels(self,image_content):
        # 인증
        credentials = self.authenticate_service_account()

        # 이미지 데이터 디코딩(즉 바이너리 데이타:bytes타입)
        # image_content = base64.b64decode(base64Encoded)

        # 이미지 파일 Vision API로 전송
        client = vision.ImageAnnotatorClient(credentials=credentials)
        image = vision.Image(content=image_content)

        # OCR 수행
        response = client.text_detection(image=image)
        texts = response.text_annotations
        responseTexts = []

        # 추출된 텍스트 출력
        if texts:
            extracted_text = texts[0].description
            responseTexts.append(extracted_text)
        else:
            print("텍스트를 추출할 수 없습니다.")
        return responseTexts

    def post(self):
        try:
            # request에서 파일 데이터를 가져옴
            file_data = request.files['data'].read()
            # Base64로 인코딩
            encoded_image = base64.b64encode(file_data).decode('utf-8')
            # OCR 수행
            texts = self.detect_labels(file_data)
            result_text = ''.join(texts)

            # 텍스트 정렬
            sorted_recipe = self.sort_by_number(result_text)
            print(sorted_recipe)

            return make_response(sorted_recipe)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

    def custom_sort_key(self, line):
        # 정규 표현식을 사용하여 라인에서 첫 번째로 발견되는 숫자를 찾음
        match = re.search(r'\b\d+\b', line)

        if match:
            # 숫자가 발견된 경우, 해당 숫자를 정수로 변환하여 반환
            return int(match.group())
        else:
            # 숫자가 없는 경우, 무한대로 설정하여 나중에 처리할 수 있도록 함
            return float('inf')

    def sort_by_number(self, text):
        lines = text.split('\n')[1:]

        # 정규식을 사용하여 숫자를 기준으로 텍스트 정렬
        sorted_lines = sorted(lines, key=lambda x: (self.custom_sort_key(x), x.strip()))
        print("sorted_lines:", sorted_lines)

        # 조건에 따라 줄바꿈을 처리하여 텍스트 생성
        sorted_text = ''
        for i, line in enumerate(sorted_lines):
            if not re.match(r'^\d', line):
                sorted_text += ' ' + line.strip()
            else:
                if i > 0 and not re.match(r'^\d', sorted_lines[i - 1]):
                    sorted_text += '\n' + line
                else:
                    sorted_text += f"{line.strip()}\n"

        # JSON 형식으로 변환하여 반환
        result_json = {"text": sorted_text}
        return json.dumps(result_json, ensure_ascii=False, indent=2)