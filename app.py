import hashlib
import json
from unittest import result
from flask import Flask, jsonify, redirect, render_template, request
from flask_cors import CORS
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.turtle
app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})


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

        return jsonify({"result": "회원가입 완료!!!"})
    else:
        return redirect('index.html')
        # return render_template('index.html')


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

@app.route("/signup/check_id", methods=["POST"])
def check_id():
    data = json.loads(request.data)
    id = data.get("id")
    duplicated_id = db.users.find_one({'id': id})

    return jsonify({"duplicated": bool(duplicated_id)})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
