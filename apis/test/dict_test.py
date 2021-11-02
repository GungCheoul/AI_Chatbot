import pickle
from utils.preprocess import Preprocess

f = open('../train_tools/dict/chatbot_dict.bin', 'rb')
word_index = pickle.load(f)
f.close()

sent = '요즘 너무 우울한 기분이 들어'

p = Preprocess(userdic='../utils/user_dic.tsv')

pos = p.pos(sent)

keywords = p.get_keywords(pos, without_tag=True)
for word in keywords:
    try:
        print(word, word_index[word])
    except KeyError:
        print(word, word_index['OOV'])
