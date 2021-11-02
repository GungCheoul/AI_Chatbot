from utils.preprocess import Preprocess
from models.ner.nermodel import NerModel

p = Preprocess(word2index_dic='./train_tools/dict/chatbot_dict.bin', userdic='./utils/user_dic.tsv')

ner = NerModel(model_name='./models/ner/ner_model.h5', proprocess=p)
# query = '왜 이렇게 화가 나지?'
query = '화만 나네'
predicts = ner.predict(query)
tags = ner.predict_tags(query)
print(predicts)
print(tags)
