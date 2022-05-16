import hashlib
import json
from unittest import result
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from pymongo import MongoClient
# import jwt

client = MongoClient('localhost', 27017)
db = client.turtle
app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
# SECRET_KEY = 'SPARTA'


# # def check_token():
# #     # 현재 이용자의 컴퓨터에 저장된 cookie 에서 mytoken 을 가져옵니다.
# #     token_receive = request.cookies.get('token')
# #     # token을 decode하여 payload를 가져오고, payload 안에 담긴 유저 id를 통해 DB에서 유저의 정보를 가져옵니다.
# #     payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
# #     return db.users.find_one({'id': payload['id']})


@app.route("/")
def hello_world():
    return jsonify({'message': 'success'})


@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    data = json.loads(request.data)
    if request.method == "POST":
        id = data.get("id")
        pw = data.get("pw")
        pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()

        doc = {
            "id": id,
            "pw": pw_hash,
        }

        db.users.insert_one(doc)

        return jsonify({"result": "회원가입 완료"})
    else:
        return render_template('index.html')


# @app.route("/signup", methods=["POST"])
# def sign_up():
    # # 1. form-data 입력 방식
    # print(request)
    # print(request.form)
    # print(request.form['id'])  # id값을 못찾으면 오류남
    # print(request.form.get('pw'))  # id값을 못찾아도 오류 안남
    # return jsonify({'message': 'success'})

    # # 2. json 입력 방식
    # data = json.loads(request.data)
    # print(data)
    # print(data.get('id'))
    # print(data.get('pw'))
    # return jsonify({'message': 'success'})

# @app.route('/login')
# def login():
#     return render_template('login.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
