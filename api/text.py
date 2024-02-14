from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from konlpy.tag import Okt
from flask_restful import Resource,reqparse
import pickle

# 불용어
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

# Okt 객체 생성
okt = Okt()

# 토크나이저 불러오기
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# 임의의 고정된 길이 설정
max_len = 100 # 이 값을 주피터 노트북에서 설정한 값과 동일하게 설정해주세요.

# 모델 로드
loaded_model = load_model('best_model.h5')

# 텍스트 감정 분석을 수행하는 함수
def sentiment_predict(new_sentence):
    new_sentence = okt.morphs(new_sentence, stem=True) # 토큰화
    new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
    encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
    pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
    score = float(loaded_model.predict(pad_new)) # 예측
    return score

# 리뷰 분석 API
class Text(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('reviews', type=list, location='json')
            args = parser.parse_args()

            reviews = args['reviews']
            sentiment_scores = [sentiment_predict(review) for review in reviews]

            positive_reviews = sum(1 for score in sentiment_scores if score > 0.5)
            negative_reviews = len(sentiment_scores) - positive_reviews

            positive_ratio = positive_reviews / len(sentiment_scores) * 100
            negative_ratio = negative_reviews / len(sentiment_scores) * 100

            response = {
                'positive_reviews': positive_reviews,
                'negative_reviews': negative_reviews,
                'positive_ratio': positive_ratio,
                'negative_ratio': negative_ratio
            }
            return response, 200

        except Exception as e:
            return {'error': str(e)}, 400