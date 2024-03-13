import json

from flask import jsonify, request
from flask_restful import Resource
from openai import OpenAI
import os
import openai
# https://platform.openai.com/docs/guides/gpt/chat-completions-api의 질의어로 테스트해보자
client = OpenAI()


class ChatBot(Resource):
    
    def post(self):
        messages = [
            {"role": "system", "content": '''You are NutriMate customer service chatbot.
                The service we provide is a platform to help provide personalized digital health care services.
                In addition to diet, recipes and food
                for personal health, we can only recommend healthy exercise.
                The more health information tailored to an individual's characteristics, the better.
                When responding, you must be courteous and courteous to all users.
                If you have a question for which you do not have a clear answer, please reply 'Contact your administrator.'
                Since you are a Korean bot and most of your users are Korean, please make sure to reply using Korean.
                If the user wishes to cancel payment or reservation, please instruct the user to consult with a counselor
                 at 010-1234-1234.
                If the user desires more information, please direct them to http://localhost:5555/info. 
                If they wish to share information with others, suggest visiting http://localhost:5555
                /board/info/all/1. 
                If they are interested in engaging in conversations with people, recommend http://localhost:5555
                /board/feed/view.
                If a user asks about the website, tell them that our site is a platform that offers personalized digital 
                health management services.'''}
        ]
        try:
            content = request.json.get('content')
            response = AIChatBot(content, messages=messages)
            messages = response['messages']
            if response['status'] == 'SUCCESS':
                answer = response['messages'][len(messages) - 1]['content']
                return jsonify({"messages": answer})
        except Exception as e:
            return jsonify({'error': str(e)})


def AIChatBot(content, model='gpt-3.5-turbo', messages=[], temperature=1):
    error = None
    try:
        messages.append({'role': 'user', 'content': content})
        response = client.chat.completions.create(model=model, messages=messages)
        answer = response.choices[0].message.content
        messages.append({'role': 'assistant', 'content': answer})
        return {'status': 'SUCCESS', 'messages': messages}
    
    except openai.error.APIError as e:
        # Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        error = e
    except openai.error.APIConnectionError as e:
        # Handle connection error here
        print(f"Failed to connect to OpenAI API: {e}")
        error = e
    except openai.error.InvalidRequestError as e:
        print(f"Invalid Request to OpenAI API: {e}")
        error = e
    except openai.error.RateLimitError as e:
        # Handle rate limit error (we recommend using exponential backoff)
        print(f"OpenAI API request exceeded rate limit: {e}")
        error = e
    return {'status': 'FAIL', 'messages': error}
