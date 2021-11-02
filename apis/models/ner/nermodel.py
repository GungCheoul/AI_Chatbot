# 엔진. 개체명 인식 모듈
# 개체명 인식 모델 파일을 활용한 개체명 인식 기능

import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Model, load_model
from tensorflow.keras import preprocessing


class NerModel:
    def __init__(self, model_name, proprocess):
        # self.index_to_ner = {1: 'O', 2: 'B_DT', 3: 'B_FOOD', 4: 'I', 5: 'B_OG', 6: 'B_PS',
        #                      7: 'B_LC', 8: 'NNP', 9: 'B_TI', 0: 'PAD'}

        self.index_to_ner = {1: 'O', 2: 'B_DT', 3: 'I', 4: 'B_OG', 5: 'B_PS',
                             6: 'B_LC', 7: 'NNP', 8: 'B_TI', 9: 'B_EM', 10: 'B_ANG', 11: 'B_CT', 12: 'B_EMRCT',
                             13: 'B_PT', 14: 'B_EP', 15: 'B_VL', 16: 'B_FIRE', 17: 'B_WRY', 18: 'B_CARE',
                             19: 'B_HP', 20: 'B_SRG', 21: 'B_OK', 22: 'B_BE', 23: 'B_BODY', 24: 'B_PB',
                             25: 'B_SYM', 26: 'B_ST', 27: 'B_CC', 28: 'B_MEX', 29: 'B_MN', 30: 'B_WK',
                             31: 'B_LF', 32: 'B_SLP', 33: 'B_CH', 34: 'B_CU', 35: 'B_AL', 36: 'B_UN',
                             37: 'B_ABS', 38: 'B_SC', 39: 'B_BIRD', 40: 'B_SP', 41: 'B_SPNV', 42: 'B_PAIN',
                             43: 'B_MISS', 44: 'B_DWN', 45: 'B_MND', 46: 'B_NV', 47: 'B_TEAR', 48: 'B_STF',
                             49: 'B_EB', 50: 'B_DR', 51: 'B_CAR', 52: 'B_M', 53: 'B_NONE', 54: 'B_LOW', 55: 'B_BT',
                             56: 'B_FOOL', 57: 'B_PP', 58: 'B_CUR', 59: 'B_WORK', 60: 'B_MIND', 61: 'B_UC',
                             62: 'B_WILL', 63: 'B_SELF', 64: 'B_COM', 65: 'B_DIE', 66: 'B_CONF', 67: 'B_SH',
                             68: 'B_SHK', 69: 'B_EMP', 70: 'B_RG', 71: 'B_HI', 0: 'PAD'}

        # self.index_to_ner = {1: 'O', 2: 'B_EM', 3: 'B_ANG', 4: 'B_CT', 5: 'B_EMRCT',
        #                      6: 'B_PT', 7: 'B_EP', 8: 'B_VL', 9: 'B_FIRE', 10: 'B_WRY', 11: 'B_CARE',
        #                      12: 'B_HP', 13: 'B_SRG', 14: 'B_OK', 15: 'B_BE', 16: 'B_BODY', 17: 'B_PB',
        #                      18: 'B_SYM', 19: 'B_ST', 20: 'B_CC', 21: 'B_MEX', 22: 'B_MN', 23: 'B_WK',
        #                      24: 'B_LF', 25: 'B_SLP', 26: 'B_CH', 27: 'B_CU', 28: 'B_AL', 29: 'B_UN',
        #                      30: 'B_ABS', 31: 'B_SC', 32: 'B_BIRD', 33: 'B_SP', 34: 'B_SPNV', 35: 'B_PAIN',
        #                      36: 'B_MISS', 37: 'B_DWN', 38: 'B_MND', 39: 'B_NV', 40: 'B_TEAR', 41: 'B_STF',
        #                      42: 'B_EB', 43: 'B_DR', 44: 'B_CAR', 45: 'B_M', 46: 'B_NONE', 47: 'B_LOW', 48: 'B_BT',
        #                      49: 'B_FOOL', 50: 'B_PP', 51: 'B_CUR', 52: 'B_WORK', 53: 'B_MIND', 54: 'B_UC',
        #                      55: 'B_WILL', 56: 'B_SELF', 57: 'B_COM', 58: 'B_DIE', 59: 'B_CONF', 60: 'B_SH',
        #                      61: 'B_SHK', 62: 'B_EMP', 63: 'B_RG', 64: 'B_HI', 0: 'PAD'}

        self.model = load_model(model_name)
        self.p = proprocess

    def predict(self, query):
        pos = self.p.pos(query)
        keywords = self.p.get_keywords(pos, without_tag=True)
        sequences = [self.p.get_wordidx_sequence(keywords)]

        max_len = 40
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, padding='post', value=0, maxlen=max_len)

        predict = self.model.predict(np.array([padded_seqs[0]]))
        predict_class = tf.math.argmax(predict, axis=-1)

        tags = [self.index_to_ner[i] for i in predict_class.numpy()[0]]
        return list(zip(keywords, tags))

    def predict_tags(self, query):
        pos = self.p.pos(query)
        keywords = self.p.get_keywords(pos, without_tag=True)
        sequences = [self.p.get_wordidx_sequence(keywords)]

        max_len = 40
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, padding='post', value=0, maxlen=max_len)

        predict = self.model.predict(np.array([padded_seqs[0]]))
        predict_class = tf.math.argmax(predict, axis=-1)

        tags = []
        for tag_idx in predict_class.numpy()[0]:
            if tag_idx == 1: continue
            tags.append(self.index_to_ner[tag_idx])

        if len(tags) == 0:
            return None
        return tags
