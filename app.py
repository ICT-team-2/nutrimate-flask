from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import os
from asgiref.wsgi import WsgiToAsgi
import uvicorn
#OCR서비용
from api.ocr import OCR
#텍스트 감정분석용
from api.text import Text
#워드클라우드 생성용
from api.word import Word

app = Flask(__name__)
CORS(app,
    resources={r'*': {'origins': 'http://localhost:5555'}},
    supports_credentials=True)

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'upload')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

api = Api(app)

asgi_app = WsgiToAsgi(app)

'''
OCR
POST /ocr
'''
api.add_resource(OCR,'/ocr')
'''
Text
POST /text
'''
api.add_resource(Text, '/text')
'''
Word
POST /word
'''
api.add_resource(Word,'/word')

if __name__ == '__main__':
    uvicorn.run(asgi_app, port=2222, host='0.0.0.0')
