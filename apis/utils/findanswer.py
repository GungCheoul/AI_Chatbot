# 엔진. 답변 검색
# 답변 검색 모듈

class FindAnswer:
    def __init__(self, db):
        self.db = db

    def _make_query(self, intent_name):
        sql = "select * from chatbot_train_data"
        if intent_name != None:
            sql = sql + " where intent='{}' ".format(intent_name)

        sql = sql + " order by rand() limit 1"
        return sql

    def search(self, intent_name):
        sql = self._make_query(intent_name)
        answer = self.db.select_one(sql)

        if answer is None:
            sql = self._make_query(intent_name)
            answer = self.db.select_one(sql)

        return answer['answer'], answer['answer_add']
