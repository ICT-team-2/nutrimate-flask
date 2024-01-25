from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import os
from asgiref.wsgi import WsgiToAsgi
import uvicorn

from api.profile import ProfileResource

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'upload')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  #16MB

api = Api(app)

@app.route('/')
def home():
    return "Hello, ICT!"

api.add_resource(ProfileResource, '/profile_img')

asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    uvicorn.run(asgi_app, port=5000, host='0.0.0.0')