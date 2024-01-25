from flask import request, send_file, jsonify
from flask_restful import Resource
from openai import OpenAI
import urllib.request
import requests

client = OpenAI(
    api_key="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"
)

model = 'gpt-3.5-turbo'
dall_e_model = "dall-e-3"

def chatComplete(client, model, messages):
    response = client.chat.completions.create(model=model, messages=messages)
    return response

class ProfileResource(Resource):
    def post(self):
        prompt = request.form['prompt']
        messages = [
            {"role": "system", "content": "you are a translation expert who translates Korean into English"},
            {"role": "user", "content": prompt}
        ]
        response = chatComplete(client, model, messages)
        english = response.choices[0].message.content
        print('번역:', english)

        response = client.images.generate(
            model=dall_e_model,
            prompt=prompt,
            size="1024x1024",
            response_format='url',
            n=1,
        )
        image_url = response.data[0].url

        #이미지 다운로드
        image_data = requests.get(image_url).content
        #이미지를 URL로 저장
        with open('image.jpg', 'wb') as f:
            f.write(image_data)
        #이미지 URL 출력
        print('이미지 URL:', image_url)

        urllib.request.urlretrieve(image_url, 'image.jpg')
        return jsonify('image_url:',image_url) #이미지 URL
        #return send_file('image.jpg', mimetype='image/gif') #이미지 사진