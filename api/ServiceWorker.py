# pip install firebase-admin
from flask import request
from flask_restful import Resource,reqparse
from firebase_admin import credentials, messaging, initialize_app
import datetime, time, json

import os

# Firebase 초기화 여부를 확인하는 변수
firebase_initialized = False
#프론트 엔드에서 받은 fcm값 저장
saved_fcm_token = None

alarms = {}
# Firebase 앱 초기화 (한 번만 실행되도록)
def initialize_firebase():
    global firebase_initialized
    if not firebase_initialized:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(script_dir, '..', 'model')
        json_file_name = 'firebase_config_file.json'
        json_file_path = os.path.join( json_file_path, json_file_name)
        with open(json_file_path, 'r') as json_file:
            service_account_info = json.load(json_file)

        firebase_config = service_account_info
        cred = credentials.Certificate(firebase_config )
        initialize_app(cred)
        firebase_initialized = True
# 알림을 보낼 함수
import threading  # 스레드 사용을 위한 모듈 추가

# 사용자별 FCM 토큰 저장을 위한 딕셔너리
user_tokens = {}

# 알림을 보낼 함수
def send_notification(title, body, image_url, token):
    try:
        message = messaging.Message(
            data={
                'title': title,
                'body': body,
                'image': image_url,
            },
            token=token
        )
        response = messaging.send(message)
        print('Successfully sent message:', response)
        return {"success": 'TT', "message": "Notification sent successfully", "response": response}, 200
    except Exception as e:
        print('Error sending message:', e)
        return {"success": False, "error": str(e)}, 500

# 알람 예약 및 처리 함수
def schedule_notification_worker(alarmId, alarm_time, title, body, image_url, token):
    current_time = datetime.datetime.now()
    alarm_datetime = datetime.datetime.strptime(alarm_time, "%Y-%m-%dT%H:%M")
    print(alarmId)
    print(token)

    if alarm_datetime >= current_time:
        time_difference = (alarm_datetime - current_time).total_seconds()
        while time_difference > 0 and alarms[alarmId]['is_active']:
            time.sleep(min(10, time_difference))  # 10초마다 is_active 상태 확인
            time_difference = (alarm_datetime - datetime.datetime.now()).total_seconds()
        if alarms[alarmId]['is_active']:
            send_notification(title, body, image_url, token)
    else:
        print("Invalid alarm time. Please choose a future time.")

def cancel_alarm(alarmId):
    if alarmId in alarms:
        alarms[alarmId]['is_active'] = False
        print(f"Alarm {alarmId} is canceled.")
    else:
        print("Alarm not found.")

# 스케줄링 - 사용자로부터 입력받은 시간에 알림을 예약하는 함수
def schedule_notification(alarm_time, title, body, image_url, token, alarmId):
    alarms[alarmId] = {
        'is_active': True,
        'thread': threading.Thread(target=schedule_notification_worker, args=(alarmId, alarm_time, title, body, image_url, token))
    }
    alarms[alarmId]['thread'].start()

class ServiceWorker(Resource):
    def __init__(self):
        initialize_firebase()
        super(ServiceWorker, self).__init__()

    def get(self):
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

            # 사용자별 토큰 저장
            user_tokens[token] = token

            # 서비스워커 백그라운드 메시지로 알림 보내기
            send_notification(title, body, image_url, token)
            #return {"success": True, "message": "Notification sent successfully"}, 200
        except Exception as e:
            return {"success": False, "error": str(e)}, 500

    # 스케줄링
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('alarm_time', type=str, required=True, help='Alarm time cannot be blank')
            parser.add_argument('title', type=str, required=True, help='Title cannot be blank')
            parser.add_argument('body', type=str, required=True, help='Body cannot be blank')
            parser.add_argument('image_url', type=str, required=True, help='Image URL cannot be blank')
            parser.add_argument('token', type=str, required=True, help='Token cannot be blank')
            parser.add_argument('alarmId', type=str, required=True, help='Token cannot be blank')

            args = parser.parse_args()

            alarm_time = args['alarm_time']
            title = args['title']
            body = args['body']
            image_url = args['image_url']
            token = args['token']
            alarmId = args['alarmId']

            # 알림 예약하기
            schedule_notification(alarm_time, title, body, image_url, token, alarmId)
            #return {"success": True, "message": "Notification scheduled successfully"}, 200


        except Exception as e:
            return {"success": False, "error": str(e)}, 500

    def delete(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('alarmId', type=str, required=True, help='Token cannot be blank')


            args = parser.parse_args()
            alarmId = args['alarmId']
            print(alarmId)
            # 알람 삭제
            cancel_alarm(alarmId)
            #return {"success": True, "message": "Notification scheduled successfully"}, 200


        except Exception as e:
            return {"success": False, "error": str(e)}, 500
