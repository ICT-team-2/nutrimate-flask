'''
1.필요한 라이브러리 설치
pip install google-cloud-vision google-auth  google-auth-oauthlib
pip install --upgrade google-auth
'''
#서비스 계정 키를 사용하여 직접 인증(토큰 인증시 유효시간이 1시간이라 1시간후에는 서비스 사용불가)
from flask_restful import Resource,reqparse
from flask import make_response
import base64
from google.cloud import vision
from google.oauth2 import service_account
import json
import os
class OCR(Resource):
    def __init__(self):
        self.credentials_path= os.environ['GOOGLE_APPLICATION_CREDENTIALS']#프로젝트 ID,Private Key정보가 있는 .json파일의 경로
    def authenticate_service_account(self):
        '''
        서비스 계정 키를 로드하여 구글 클라우드 Vision API에 인증하는 함수
        return: 인증 정보 객체
        '''
        credentials = service_account.Credentials.from_service_account_file(self.credentials_path)
        scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
        print('scoped_credentials:', scoped_credentials)
        return scoped_credentials
    def detect_labels(self,base64Encoded):
        '''
        인증후 인자로 받은 base64인코딩 문자열(base64Encoded)을 구글 서버로 전송해서
        객체 탐지 결과를 받는 함수
        base64Encoded:이미지의 BASE64인코딩 문자열
        return : 객체 탐지인 경우 JSON반환
                 OCR은 텍스트 반환
        '''
        # 인증
        # Authenticate with service account credentials
        credentials = self.authenticate_service_account()

        # 이미지 데이터 디코딩(즉 바이너리 데이타:bytes타입)
        # Decode the image data from base64

        image_content = base64.b64decode(base64Encoded)

        # 이미지 파일 Vision API로 전송
        # Create an instance of the Vision API client
        client = vision.ImageAnnotatorClient(credentials=credentials)
        # Create an image object
        image = vision.Image(content=image_content)
        # 객체 탐지
        '''
        response = client.label_detection(image=image)
        print('type(response):',type(response))#<class 'google.cloud.vision_v1.types.image_annotator.AnnotateImageResponse'>
        print('response:',response)

        labels = response.label_annotations
        print('type(labels):',type(labels))
        print('labels:',labels)
        '''
        """
        label_annotations {
            mid: "/m/05wrt"
            description: "Property"
            score: 0.941965342
            topicality: 0.941965342
            }
        label_annotations {
            mid: "/m/0c_jw"
            description: "Furniture"
            score: 0.933456
            topicality: 0.933456
        }      
        """
        '''
        # 레이블 출력
        for label in labels:
            print('객체:%s,정확도:%s' % (label.description,label.score))
        '''
        # OCR 탐지
        # OCR 수행
        response = client.text_detection(image=image)
        # print('type(response):',type(response))#<class 'google.cloud.vision_v1.types.image_annotator.AnnotateImageResponse'>
        # print('response:',response)
        texts = response.text_annotations
        # print('type(texts):',type(texts))#<class 'proto.marshal.collections.repeated.RepeatedComposite'>
        print('dir(texts):', dir(texts))
        responseTexts = []
        # 추출된 텍스트 출력
        if texts:
            extracted_text = texts[0].description
            responseTexts.append(extracted_text)
        else:
            print("텍스트를 추출할 수 없습니다.")
        return responseTexts

    def post(self):
        parser = reqparse.RequestParser()
        #base64Encoded는 파라미터명.location='form'는 데이타를 JSON이 아닌 KEY=VALUE쌍으로 받겠는다는 의미
        parser.add_argument('base64Encoded',location='form')
        args = parser.parse_args()
        #print(args['base64Encoded'])
        texts=self.detect_labels(args['base64Encoded'])
        print(''.join(texts))
        return make_response(''.join(texts))