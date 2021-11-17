from utils.preprocess import Preprocess
from models.intent.intent_model import IntentModel

p = Preprocess(word2index_dic='./train_tools/dict/chatbot_dict.bin',
               userdic='./utils/user_dic.tsv')

intent = IntentModel(model_name='./models/intent/intent_model.h5', proprocess=p)

query = '코로나19'
predict = intent.predict_class(query)
predict_label = intent.labels[predict]

print(query)
print('의도 예측 클래스: ', predict)
print('의도 예측 레이블: ', predict_label)
