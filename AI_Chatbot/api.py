from flask import Flask, request, jsonify, abort
import socket
import json

host = "127.0.0.1"
port = 5050

app = Flask(__name__)


def get_answer_from_engine(bottype, query):
    mySocket = socket.socket()
    mySocket.connect((host, port))

    json_data = {
        'Query': query,
        'BotType': bottype
    }
    message = json.dumps(json_data)
    mySocket.send(message.encode())

    data = mySocket.recv(2048).decode()
    ret_data = json.loads(data)

    mySocket.close()

    return ret_data


@app.route('/', methods=['GET'])
def index():
    return 'hello', 200


@app.route('/query/<bot_type>', methods=['POST'])
def query(bot_type):
    body = request.get_json()

    try:
        if bot_type == "KAKAO":
            body = request.get_json()
            utterance = body['userRequest']['utterance']
            ret = get_answer_from_engine(bottype=bot_type, query=utterance)

            from Kakao import KakaoTemplate
            skillTemplate = KakaoTemplate()
            return skillTemplate.send_response(ret)

        else:
            abort(404)

    except Exception as ex:
        abort(500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
