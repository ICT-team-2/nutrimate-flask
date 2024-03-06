from flask import request, send_file, jsonify
from flask_restful import Resource
from openai import OpenAI
import urllib.request
import requests
import base64


class ProfileResource(Resource):
    
    def __init__(self):
        self.client = OpenAI(
            api_key="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"
        )
        self.dall_e_model = "dall-e-3"
    
    def post(self):
        prompt = request.form['prompt']
        
        response = self.client.images.generate(
            model=self.dall_e_model,
            # prompt="a white siamese cat",
            prompt=prompt,
            size="1024x1024",
            quality="hd",
            response_format="b64_json"
        )
        
        image_url = response.data[0].b64_json
        # filename = f'{prompt}.jpg'
        # # 이미지를 URL로 저장
        # with open(filename, 'wb') as f:
        #     f.write(base64.b64decode(image_url))
        
        return jsonify({'image': image_url})  # 이미지 URL
        # return send_file('image.jpg', mimetype='image/gif') #이미지 사진
