from utils.preprocess import Preprocess

sent = '요즘 너무 우울한 기분이 들어'

p = Preprocess(userdic='../utils/user_dic.tsv')

pos = p.pos(sent)

ret = p.get_keywords(pos, without_tag=False)
print(ret)

ret = p.get_keywords(pos, without_tag=True)
print(ret)
