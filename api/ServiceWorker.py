# pip install firebase-admin

from flask import request
from flask_restful import Resource,reqparse
from firebase_admin import credentials, messaging, initialize_app
import datetime, time
import os

# Firebase 초기화 여부를 확인하는 변수
firebase_initialized = False

# Firebase 앱 초기화 (한 번만 실행되도록)
def initialize_firebase():
    global firebase_initialized
    if not firebase_initialized:
        service_account_info = os.environ.get('GOOGLE_APPLICATION_SERVICEWORKER')
        cred = credentials.Certificate(service_account_info)
        initialize_app(cred)
        firebase_initialized = True

# 알림을 보낼 함수
def send_notification(title, body, image_url, token):
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
                image=image_url,
            ),
            token=token
        )
        # 이곳의 코드가 반환된다
        response = messaging.send(message)
        print('Successfully sent message:', response)
        return {"success": True, "message": "Notification sent successfully", "response": response}, 200
    except Exception as e:
        print('Error sending message:', e)
        return {"success": False, "error": str(e)}, 500

# 스케줄링 - 사용자로부터 입력받은 시간에 알림을 예약하는 함수
def schedule_notification(alarm_time, title, body, img_url, token):
    current_time = datetime.datetime.now()
    alarm_datetime = datetime.datetime.strptime(alarm_time, "%Y-%m-%dT%H:%M")

    # 입력받은 시간이 현재 시간 이후인지 확인
    if alarm_datetime > current_time:
        time_difference = (alarm_datetime - current_time).total_seconds()

        # 입력받은 시간까지 대기 후 알림 보내기
        time.sleep(time_difference)
        send_notification(title, body, img_url, token)
    else:
        print("Invalid alarm time. Please choose a future time.")

class ServiceWorker(Resource):
    def __init__(self):
        initialize_firebase()
        super(ServiceWorker, self).__init__()
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('title', type=str, required=True, help='Title cannot be blank')
            parser.add_argument('body', type=str, required=True, help='Body cannot be blank')
            parser.add_argument('image_url', type=str, required=True, help='Image URL cannot be blank')
            parser.add_argument('token', type=str, required=True, help='Token cannot be blank')

            args = parser.parse_args()

            title = args['title']
            body = args['body']
            image_url = args['image_url']
            token = args['token']

            # 서비스워커 백그라운드 메시지로 알림 보내기
            send_notification(title, body, image_url, token)
            return {"success": True, "message": "Notification sent successfully"}, 200
        except Exception as e:
            return {"success": False, "error": str(e)}, 500

    # 스케줄링
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('alarm_time', type=str, required=True, help='Alarm time cannot be blank')
            parser.add_argument('title', type=str, required=True, help='Title cannot be blank')
            parser.add_argument('body', type=str, required=True, help='Body cannot be blank')
            parser.add_argument('image_url', type=str, required=True, help='Image URL cannot be blank')
            parser.add_argument('token', type=str, required=True, help='Token cannot be blank')

            args = parser.parse_args()

            alarm_time = args['alarm_time']
            title = args['title']
            body = args['body']
            image_url = args['image_url']
            token = args['token']

            # 알림 예약하기
            schedule_notification(alarm_time, title, body, image_url, token)
            return {"success": True, "message": "Notification scheduled successfully"}, 200
        except Exception as e:
            return {"success": False, "error": str(e)}, 500