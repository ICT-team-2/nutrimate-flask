# pip install firebase-admin

import firebase_admin
from firebase_admin import credentials, messaging
import os

# 환경 변수에서 서비스 계정 정보 가져오기
service_account_info = os.environ.get('GOOGLE_APPLICATION_SERVICEWORKER')

# Firebase Admin SDK 초기화
cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)

# FCM 메시지 구성
message = messaging.Message(
    notification=messaging.Notification(
        title='Test Notification',
        body='This is a test notification.'
    ),
    token='fmfDTH8LcTAMHVmEgC2NkK:APA91bFMGkGdhorldNd4CY8Owi7LAmWQzSyBOVYc4l8kVGhEipJ9SEpEl3gUA8WTa4Vpa3p9QQZGNUJOcj16Ii2EYb9lBLvsI4ZDre-BJdOY7nDLPUU_1XVHHfhC-Fq9mokKRezWZymQ'  # 알림을 받을 디바이스의 FCM 토큰
)

# FCM 알림 전송
try:
    response = messaging.send(message)
    print('Successfully sent message:', response)
except Exception as e:
    print('Error sending message:', e)