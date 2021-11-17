# 엔진 전체 동작
# 전처리 -> 의도 분류 -> 개체명 인식 -> 답변 검색

from config.DB_Config import *
from utils.database import Database
from utils.preprocess import Preprocess

p = Preprocess(word2index_dic='./train_tools/dict/chatbot_dict.bin', userdic='./utils/user_dic.tsv')

db = Database(
    host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db_name=DB_NAME
)
db.connect()

query = '왜 이렇게 짜증만 날까'

from models.intent.intent_model import IntentModel
intent = IntentModel(model_name='./models/intent/intent_model.h5', proprocess=p)
predict = intent.predict_class(query)
intent_name = intent.labels[predict]

print('질문 : ', query)
print('=' * 40)
print('의도 파악 : ', intent_name)
print('=' * 40)


from utils.findanswer import FindAnswer
try:
    f = FindAnswer(db)
    answer, answer_add = f.search(intent_name)
except:
    answer = '죄송해요, 무슨 말인지 모르겠어요.'

print('답변 : ', answer)

db.close()
