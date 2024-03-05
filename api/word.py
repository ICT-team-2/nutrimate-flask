# word.py
from flask_restful import Resource
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from konlpy.tag import Kkma
import base64

class Word(Resource):
    def post(self):
        try:
            # CSV 파일에서 리뷰들을 읽어오기
            df = pd.read_csv('reviews.csv', names=['review'], encoding='utf-8')

            df['review'] = df['review'].str.replace('[^가-힣]', ' ', regex=True)

            kkma = Kkma() # 형태소 분석기

            nouns = df['review'].apply(kkma.nouns)
            nouns = nouns.explode()

            df_word = pd.DataFrame({'word': nouns})
            df_word['count'] = df_word['word'].str.len()
            df_word = df_word.query('count >= 2')
            df_word = df_word.groupby('word', as_index=False).count().sort_values('count', ascending=False)

            df_word = df_word.iloc[3:, :]
            dic_word = df_word.set_index('word').to_dict()['count']

            wc = WordCloud(random_state=123, font_path='NanumGothic', width=400, height=400, background_color='white')

            img_wordcloud = wc.generate_from_frequencies(dic_word)

            plt.figure(figsize=(10, 10)) # 크기 지정하기
            plt.axis('off') # 축 없애기
            plt.imshow(img_wordcloud) # 결과 보여주기
            filepath = '워드클라우드.png'
            plt.savefig(filepath) # 파일 저장
            plt.close()  # 이미지 파일 닫기
            # 이미지 파일을 base64로 변환
            with open(filepath, 'rb') as file:
                image_data = file.read()
                base64_data = base64.b64encode(image_data).decode('utf-8')

            # 응답으로 base64 이미지 데이터 반환
            return {'message': 'Word cloud generated successfully', 'image_base64': base64_data}, 200

        except Exception as e:
            return {'error': str(e)}, 400