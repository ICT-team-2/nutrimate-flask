# word.py
from flask_restful import Resource
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from konlpy.tag import Kkma
import base64
import cx_Oracle
import configparser
from PIL import Image

class Word(Resource):
    def get(self):
        try:
            # CSV 파일에서 리뷰들을 읽어오기
            config = configparser.ConfigParser()
            result = config.read('oracle.ini', encoding='utf8')

            with cx_Oracle.connect(user=config['ORACLE']['USER'],
                                   password=config['ORACLE']['PASSWORD'],
                                   dsn=config['ORACLE']['URL'], encoding="UTF-8") as conn:
                # 3.쿼리 실행을 위한 커서객체 얻기
                cursor = conn.cursor()
                # 4.쿼리 실행
                cursor.execute(''' SELECT b.board_category, b.board_content, b.board_title, c.cmt_content, ht.tag_name
                                    FROM board b 
                                    full join comments c ON b.board_id = c.board_id 
                                    full join BOARD_HASHTAG bh ON b.board_id = bh.board_id 
                                    full join hashTag ht ON ht.tag_id = bh.tag_id
                                    WHERE c.blocked = 'N' AND c.deleted = 'N'
            		        ''')
                # 5.패치
                rows = cursor.fetchall()
                boardContent = []
                for row in rows:
                    boardContent.append(row[0])
                    boardContent.append(row[1])
                    boardContent.append(row[2])
                    boardContent.append(row[3])
                    boardContent.append(row[4])
    
            df = pd.DataFrame(boardContent, columns=['review'])
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