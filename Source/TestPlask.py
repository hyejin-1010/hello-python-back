# app.py
from crypt import methods
from urllib import request
from flask import Flask, render_template

#Flask 객체3 인스턴스 생성
app = Flask(__name__)

@app.route('/') # 접속하는 url
def index():
  return render_template('index.html')

@app.route('/HelloWorld/') # 접속하는 url
def HelloWorld():
  return "HelloWorld"

@app.route('/register_page/', methods=['POST']) #회원가입 정보 수신
def register() :
  id_receive = request.form['id_give']
  pw_receive = request.form['pw_give']
  nickname_receive = request.form['nickname_receive']


@app.route('/login_page/', methods=['POST']) #login 정보 수신
def login() :
  id_receive = request.form['id_give']
  pw_receive = request.form['pw_give']

if __name__=="__main__":
  app.run(debug=False)
  # host 등을 직접 지정하고 싶다면
  # app.run(host="127.0.0.1", port="5000", debug=True)
  