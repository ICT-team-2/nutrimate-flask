# notification_scheduler.py
import datetime
import time
from firebase_admin import messaging

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
        response = messaging.send(message)
        print('Successfully sent message:', response)
        return {"success": True, "message": "Notification sent successfully", "response": response}, 200
    except Exception as e:
        print('Error sending message:', e)
        return {"success": False, "error": str(e)}, 500

def schedule_notification(alarm_time, title, body, img_url, token):
    current_time = datetime.datetime.now()
    alarm_datetime = datetime.datetime.strptime(alarm_time, "%Y-%m-%dT%H:%M")

    if alarm_datetime > current_time:
        time_difference = (alarm_datetime - current_time).total_seconds()
        time.sleep(time_difference)
        send_notification(title, body, img_url, token)
    else:
        print("Invalid alarm time. Please choose a future time.")
