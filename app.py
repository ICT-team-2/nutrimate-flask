from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import os
from asgiref.wsgi import WsgiToAsgi
import uvicorn

from api.profile import ProfileResource

from api.ChatBot import ChatBot
# OCR서비스용
from api.ocr import OCR
# ServiceWorker서비스용
from api.ServiceWorker import ServiceWorker

from api.recipe import RecipeResource

from api.news import Navernews, Exercise, Nutrients

# 식당 추천
from api.restaurant import RestaurantRecommend
# 헬스장 추천
from api.gym import GymRecommend

from api.foodDetection import FoodDetection




app = Flask(__name__)
CORS(app,
    resources={r'*': {'origins': 'http://localhost:5555'}},
    supports_credentials=True)

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'upload')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

api = Api(app)


@app.route('/')
def home():
    return "Hello, ICT!"


asgi_app = WsgiToAsgi(app)

api.add_resource(ChatBot, '/chatbot')
api.add_resource(Navernews, '/navernews')
api.add_resource(Exercise, '/exercise-info')
api.add_resource(Nutrients, '/nutrients-info')

api.add_resource(RestaurantRecommend, '/restaurant')
api.add_resource(GymRecommend, '/gym')

'''
OCR
POST /ocr
'''
api.add_resource(OCR, '/ocr')

'''
ServiceWorker
Post /serviceworker
'''

api.add_resource(ServiceWorker, '/serviceworker')
api.add_resource(ProfileResource, '/profile/img')
api.add_resource(RecipeResource, '/recipe-info')

api.add_resource(FoodDetection, '/food')

if __name__ == '__main__':
    uvicorn.run(asgi_app, port=2222, host='0.0.0.0')
