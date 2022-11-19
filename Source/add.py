from math import fabs
import os
import tempfile #디렉토리 절대 경로
from flask import Flask
from flask import jsonify #jsonify
from flask import request #회원정보를 제출할 때 쓰는 request, post요청 처리
from flask import redirect #리다이렉트
from flask import session #세션
from flask_wtf.csrf import CSRFProtect #csrf
from werkzeug.utils import secure_filename
app = Flask(__name__)

#다른 .py 임포트
from models import User, Learning, PointGame

@app.route('/', methods=['GET']) # 메인페이지
def mainpage():
  userid = session.get('userid', None)
  userdata = User.GetUserData(userid)
  if userdata is None : 
    flag = False
  else :    #user 정보 return
    flag = True

  return jsonify(
    { "success" : flag,
      "data" : userdata})

@app.route('/register/', methods=['GET','POST']) #회원가입
def register() :
  if request.method == 'POST' :
    if request.is_json :
      userid = request.json['userid']
      nickname = request.json['nickname']
      password = request.json['password']

      flag = User.RegisterData(userid, nickname, password)

      data = {  
        "success" : flag,
        "data" : {
          "userid" : userid,
          "nickname" : nickname,
          "password" : password
        }
      }
      return jsonify(data)

@app.route('/deleteUser/', methods=['GET','POST']) #삭제
def deleteUser() :
  User.DeleteData(session['userid'])
  return redirect('/')

@app.route('/login/', methods=['GET','POST']) #login
def login() :
  if request.method == 'POST' :
    if request.is_json :
      userid = request.json['userid']
      password = request.json['password']

      flag = User.LoginData(userid, password)
      session['userid'] = userid  #세션에 로그인 정보 저장

      data = {
        "success" : flag,
        "data" : {
          "userid" : userid,
          "password" : password
        }
      }
      return jsonify(data)

@app.route('/logout/') 
def logout() : #logout
  session.pop('userid', None)
  User.LogoutData()
  return redirect('/')

@app.route('/userInform/', methods=['GET', 'POST'])  #사용자 정보 수정
def getUserData() : 
  if session.get('userid') is None : 
    return redirect('/login/')

  userdata = User.GetUserData(session.get('userid'))
  if userdata is None : 
    flag = False  #"User 정보가 없습니다."
  else : 
    flag = True
    
  if request.method == 'GET' : 
    pass
  elif request.method == 'POST' :
    if request.is_json :
      newPicture = request.json['newProfileImage'] #json 이미지 변환?
      
      pictureImage = request.files['file']

      temp = tempfile.NamedTemporaryFile(delete=False)
      pictureImage.save(temp.name)
      
      User.SetProfileImage(session.get('userid'), temp.name)
      os.remove(temp.name)
      
  return jsonify(
    { "success" : flag,
      "data" : userdata})

@app.route('/admin_LearningData/', methods=['GET'])
def allLearningData() : 
  if request.method == 'GET' : 
    data = Learning.AllData()

    return jsonify (
      {
        "success" : data != None, 
        "data" : data
      })

@app.route('/admin_LearningData/add/', methods=['POST'])
def addLearningData() : 
  #admin 외 접근 제한 필요
  if request.method == 'POST' :
    learning = Learning()
    learning.learningID = request.json['learningID']
    learning.Title = request.json['Title']
    learning.video = request.json['video']
    learning.pointGameIDs = request.json['pointGameIDs']

    return jsonify (
      {
        "success" : learning.addLearning(), 
        "data" : learning.getData()
      })

@app.route('/admin_LearningData/edit/', methods=['GET','POST'])
def editLearningData() : 
  #admin 외 접근 제한 필요
  if request.method == 'GET' : 
    uid = request.json['learningID']
    data = Learning.findLearningData(uid)
    
    return jsonify (
      {
        "success" : data != None, 
        "data" : data
      })
  elif request.method == 'POST' :
    learning = Learning()
    learning.learningID = request.json['learningID']
    learning.Title = request.json['Title']
    learning.video = request.json['video']
    learning.pointGameIDs = request.json['pointGameIDs']

    return jsonify (
      {
        "success" : learning.editLearning(), 
        "data" : learning.getData()
      })

@app.route('/admin_LearningData/delete/', methods=['POST'])
def deleteLearningData() : 
  #admin 외 접근 제한 필요
  if request.method == 'POST' :
    learningID = request.json['learningID']

    return jsonify (
      {
        "success" : Learning.deleteLearning(learningID)
      })

@app.route('/admin_PointGameData/', methods=['GET'])
def allPointGameData() : 
  if request.method == 'GET' : 
    data = PointGame.AllData()

    return jsonify (
      {
        "success" : data != None, 
        "data" : data
      })

@app.route('/admin_PointGameData/add/', methods=['POST'])
def addPointGameData() : 
  #admin 외 접근 제한 필요
  if request.method == 'POST' :
    pointGame = PointGame()
    pointGame.pointGameID = request.json['pointGameID']
    pointGame.title = request.json['title']
    pointGame.description = request.json['description']
    pointGame.content = request.json['content']
    pointGame.answer = request.json['answer']
    pointGame.selection = request.json['selection']
    pointGame.hint = request.json['hint']
    pointGame.earnPoint = request.json['earnPoint']

    return jsonify (
      {
        "success" : pointGame.addPointGame(), 
        "data" : pointGame.getData()
      })

@app.route('/admin_PointGameData/edit/', methods=['GET','POST'])
def editPointGameData() : 
  #admin 외 접근 제한 필요
  if request.method == 'GET' : 
    uid = request.json['pointGameID']
    data = PointGame.finePointGame(uid)
    
    return jsonify (
      {
        "success" : data != None, 
        "data" : data
      })
  elif request.method == 'POST' :
    pointGame = PointGame()
    pointGame.pointGameID = request.json['pointGameID']
    pointGame.title = request.json['title']
    pointGame.description = request.json['description']
    pointGame.content = request.json['content']
    pointGame.answer = request.json['answer']
    pointGame.selection = request.json['selection']
    pointGame.hint = request.json['hint']
    pointGame.earnPoint = request.json['earnPoint']

    return jsonify (
      {
        "success" : pointGame.editPointGame(), 
        "data" : pointGame.getData()
      })

@app.route('/admin_PointGameData/delete/', methods=['POST'])
def deletePountGameData() : 
  #admin 외 접근 제한 필요
  if request.method == 'POST' :
    pointGameID = request.json['pointGameID']

    return jsonify (
      {
        "success" : PointGame.deletePointGame(pointGameID)
      })


if __name__=="__main__":
  # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
  app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True #사용자에게 정보 전달완료하면 teadown. 그 때마다 커밋=DB반영
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #추가 메모리를 사용하므로 꺼둔다
  app.config['SECRET_KEY']='asdfasdfasdfqwerty' #해시값은 임의로 적음
  app.config['UPLOAD_FOLDER'] = 'upload'
  ALLOW_EXTENSION = set(['png','jpg'])

  #csrf = CSRFProtect()
  #csrf.init_app(app)

  app.run(debug=False)  # host 등을 직접 지정하고 싶다면 app.run(host="127.0.0.1", port="5000", debug=True)
