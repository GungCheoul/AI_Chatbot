import threading
import json

from config.DB_Config import *
from utils.database import Database
from utils.engine_server import BotServer
from utils.preprocess import Preprocess
from models.intent.intent_model import IntentModel
from utils.findanswer import FindAnswer
from bs4 import BeautifulSoup
import urllib.request as req

p = Preprocess(word2index_dic='train_tools/dict/chatbot_dict.bin',
               userdic='utils/user_dic.tsv')

intent = IntentModel(model_name='models/intent/intent_model.h5', proprocess=p)


def to_client(conn, addr, params):
    db = params['db']

    try:
        db.connect()

        read = conn.recv(2048)
        print('===========================')
        print('Connection from: %s' % str(addr))

        if read is None or not read:
            print('클라이언트 연결 끊어짐')
            exit(0)


        recv_json_data = json.loads(read.decode())
        print("데이터 수신 : ", recv_json_data)
        query = recv_json_data['Query']

        intent_predict = intent.predict_class(query)
        intent_name = intent.labels[intent_predict]

        try:
            f = FindAnswer(db)
            answer, answer_add = f.search(intent_name)
            if intent_name == '코로나19':
                code_num = req.urlopen('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%ED%99%95%EC%A7%84%EC%9E%90')
                soup_num = BeautifulSoup(code_num, 'html.parser')
                info_num = soup_num.select('div.status_info em')
                code_news = req.urlopen('https://search.naver.com/search.naver?where=news&sm=tab_jum&query=%EC%BD%94%EB%A1%9C%EB%82%98')
                soup_news = BeautifulSoup(code_news, 'html.parser')
                title_list = soup_news.select('a.news_tit')
                output_result = ''
                for i in title_list:
                    title = i.text
                    news_url = i.attrs['href']
                    output_result += title + '\n' + news_url + '\n\n'
                    if title_list.index(i) == 2:
                        break
                answer = answer + info_num[0].string + '명\n\n[코로나 관련 뉴스]\n\n' + output_result

        except:
            answer = "죄송해요. 무슨 말인지 모르겠어요."
            answer_add = None

        send_json_data_str = {
            "Query": query,
            "Answer": answer,
            "AnswerImageUrl": answer_add,
            "Intent": intent_name,
        }
        message = json.dumps(send_json_data_str)
        conn.send(message.encode())

    except Exception as ex:
        print(ex)

    finally:
        if db is not None:
            db.close()
        conn.close()


if __name__ == '__main__':

    db = Database(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db_name=DB_NAME
    )
    print("========== DB 접속 ==========")

    port = 5050
    listen = 100

    bot = BotServer(port, listen)
    bot.create_sock()
    print(" *** chatbot engine server start *** ")

    while True:
        conn, addr = bot.ready_for_client()
        params = {
            "db": db
        }

        client = threading.Thread(target=to_client, args=(
            conn,
            addr,
            params
        ))
        client.start()
