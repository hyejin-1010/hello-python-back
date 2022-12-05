from math import fabs
import os
import tempfile #디렉토리 절대 경로
from flask import Flask
from flask import jsonify #jsonify
from flask import request #회원정보를 제출할 때 쓰는 request, post요청 처리
from flask import redirect #리다이렉트
from flask import session #세션
#from flask_wtf.csrf import CSRFProtect #csrf
from werkzeug.utils import secure_filename
from io import BytesIO
from PIL import Image
import base64
from flask_cors import CORS
import json

app = Flask(__name__)

#다른 .py 임포트
from models import User, Learning, PointGame, Dice

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
    body = GetJsonData(request)

    userid = body['userid']
    nickname = body['nickname']
    password = body['password']

    flag = User.RegisterData(userid, nickname, password)
    userData =  User.changeData(User.GetUserData(userid))

    data = {  
      "success" : flag,
      "data" : userData,
    }
    return jsonify(data)
  
@app.route('/register/idCheck', methods=['POST']) #회원가입 중복 체크
def idDoubleCheck() :
  if request.method == 'POST' :
    body = GetJsonData(request)

    userid = body['userid']

    flag = User.RegisterDoubleCheck(userid)

    data = {  
      "success" : flag, #True: 가입 가능/ False: 중복 있음
      "data" : body,
    }
    return jsonify(data)

@app.route('/deleteUser/', methods=['GET','POST']) #삭제
def deleteUser() :
  if session.get('userid') is None : 
    flag = False
  else :
    flag = User.DeleteData(session['userid'])
  return jsonify (
    {
      "success" : flag, 
    })

@app.route('/login/', methods=['GET','POST']) #login
def login() :
  if request.method == 'POST' :
    body = GetJsonData(request)

    userid = body['userid']
    password = body['password']

    flag = User.LoginData(userid, password)
    userData =  User.changeData(User.GetUserData(userid))
    session['userid'] = userid  #세션에 로그인 정보 저장

    data = {
      "success" : flag,
      "data" : userData,
    }
    return jsonify(data)

@app.route('/logout/') 
def logout() : #logout
  if session.get('userid') is None : 
    flag = False
  else :
    session.pop('userid', None)
    flag = True
  return jsonify (
    {
      "success" : flag, 
    })

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
    body = GetJsonData(request)

    img = body['newProfileImage']   # Base64로 변환된 File 읽어옴
    img = base64.b64decode(img)
    img = BytesIO(img)
    img = Image.open(img)
    
    temp = tempfile.NamedTemporaryFile(delete=False)
    img.save(temp.name + '.png')
    
    User.SetProfileImage(session.get('userid'), temp.name + '.png')
    os.remove(temp.name + '.png')
      
  return jsonify(
    { "success" : flag,
      "data" : userdata})


@app.route('/doneLearning/', methods=['POST'])  #학습완료 업데이트
def doneLearning() : 
  body = GetJsonData(request)
  flag = User.addCompleteData(body['userid'], body['learningID'])

  return jsonify(
    {
        "success" : flag
    })

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
    body = GetJsonData(request)

    learning = Learning()
    learning.learningID = body['learningID']
    learning.Title = body['Title']
    learning.video = body['video']
    learning.pointGameIDs = body['pointGameIDs']

    return jsonify (
      {
        "success" : learning.addLearning(), 
        "data" : learning.getData()
      })

@app.route('/admin_LearningData/edit/', methods=['GET','POST'])
def editLearningData() : 
  #admin 외 접근 제한 필요
  if request.method == 'GET' : 
    body = GetJsonData(request)

    uid = body['learningID']
    data = Learning.findLearningData(uid)
    
    return jsonify (
      {
        "success" : data != None, 
        "data" : data
      })
  elif request.method == 'POST' :
    body = GetJsonData(request)

    learning = Learning()
    learning.learningID = body['learningID']
    learning.Title = body['Title']
    learning.video = body['video']
    learning.pointGameIDs = body['pointGameIDs']

    return jsonify (
      {
        "success" : learning.editLearning(), 
        "data" : learning.getData()
      })

@app.route('/admin_LearningData/delete/', methods=['POST'])
def deleteLearningData() : 
  #admin 외 접근 제한 필요
  if request.method == 'POST' :
    body = GetJsonData(request)
    learningID = body['learningID']

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
    body = GetJsonData(request)

    pointGame = PointGame()
    pointGame.pointGameID = body['pointGameID']
    pointGame.title = body['title']
    pointGame.description = body['description']
    pointGame.content = body['content']
    pointGame.answer = body['answer']
    pointGame.selection = body['selection']
    pointGame.hint = body['hint']
    pointGame.earnPoint = body['earnPoint']

    return jsonify (
      {
        "success" : pointGame.addPointGame(), 
        "data" : pointGame.getData()
      })

@app.route('/admin_PointGameData/edit/', methods=['GET','POST'])
def editPointGameData() : 
  #admin 외 접근 제한 필요
  if request.method == 'GET' : 
    body = GetJsonData(request)

    uid = body['pointGameID']
    data = PointGame.finePointGame(uid)
    
    return jsonify (
      {
        "success" : data != None, 
        "data" : data
      })
  elif request.method == 'POST' :
    body = GetJsonData(request)

    pointGame = PointGame()
    pointGame.pointGameID = body['pointGameID']
    pointGame.title = body['title']
    pointGame.description = body['description']
    pointGame.content = body['content']
    pointGame.answer = body['answer']
    pointGame.selection = body['selection']
    pointGame.hint = body['hint']
    pointGame.earnPoint = body['earnPoint']

    return jsonify (
      {
        "success" : pointGame.editPointGame(), 
        "data" : pointGame.getData()
      })

@app.route('/admin_PointGameData/delete/', methods=['POST'])
def deletePointGameData() : 
  #admin 외 접근 제한 필요
  if request.method == 'POST' :
    body = GetJsonData(request)
    pointGameID = body['pointGameID']

    return jsonify (
      {
        "success" : PointGame.deletePointGame(pointGameID)
      })

@app.route('/admin_DiceData/', methods=['GET'])
def allDiceData() : 
  if request.method == 'GET' : 
    data = Dice.AllData()

    return jsonify (
      {
        "success" : data != None, 
        "data" : data
      })

@app.route('/admin_DiceData/add/', methods=['POST'])
def addDiceData() : 
  #admin 외 접근 제한 필요
  if request.method == 'POST' :
    body = GetJsonData(request)

    dice = Dice()
    dice.diceID = body['diceID']
    dice.pointGameIDs = body['pointGameIDs']

    return jsonify (
      {
        "success" : dice.addDice(), 
        "data" : dice.getData()
      })

@app.route('/admin_DiceData/edit/', methods=['GET','POST'])
def editDiceData() : 
  #admin 외 접근 제한 필요
  if request.method == 'GET' : 
    body = GetJsonData(request)

    uid = body['diceID']
    data = Dice.findDice(uid)
    
    return jsonify (
      {
        "success" : data != None, 
        "data" : data
      })
  elif request.method == 'POST' :
    body = GetJsonData(request)

    dice = Dice()
    dice.diceID = body['diceID']
    dice.pointGameIDs = body['pointGameIDs']

    return jsonify (
      {
        "success" : dice.editDice(), 
        "data" : dice.getData()
      })

@app.route('/admin_DiceData/delete/', methods=['POST'])
def deleteDiceData() : 
  #admin 외 접근 제한 필요
  if request.method == 'POST' :
    body = GetJsonData(request)
    diceID = body['diceID']

    return jsonify (
      {
        "success" : Learning.deleteLearning(diceID)
      })

@app.route('/Ranking/', methods=['GET'])
def getRanking() :
  if request.method == 'GET' :
    data = User.GetRanking()
    return jsonify (
      {
        "success" : data != None, 
        "data" : data
      })
  
def GetJsonData(request) : 
  if request.is_json :
    body = request.json
  else :
    body = json.loads(request.get_data(parse_form_data=True))
  return body

@app.route('/LearningData/<learningID>') 
def getLearningData(learningID) : #각 LearningData 정보 얻어오기
  if request.method == 'GET' :
    readData = Learning.findLearningData(learningID)
    
    return jsonify (
      {
        "success" : readData != None, 
        "data" : readData
      })

@app.route('/PointGame/<pointGameID>')
def getPointGameData(pointGameID) : #각 pointGame 정보 얻어오기
  if request.method == 'GET' :
    readData = PointGame.finePointGame(pointGameID)
    
    return jsonify (
      {
        "success" : readData != None, 
        "data" : readData
      })
  
@app.route('/DiceData/<diceID>')
def getDiceData(diceID) : #각 Dice 정보 얻어오기
  if request.method == 'GET' :
    readData = Dice.findDice(diceID)
    
    return jsonify (
      {
        "success" : readData != None, 
        "data" : readData
      })
  
@app.route('/PointGames/<learningID>', methods=['GET']) 
def getPointGamesOfLearingID(learningID) : #LearningID에 따른 PointGame 가져오기
  if request.method == 'GET' :
    flag = False
    pointGameData = {}

    findData = Learning.findLearningData(learningID)
    if findData != None :
      pointGameList = list(findData.get('pointGameIDs').values())
      for ids in pointGameList : 
        pointGameData[ids] = PointGame.finePointGame(ids)
      flag = True      

    return  jsonify (
      {
        "success" : flag,
        "data" : pointGameData,
      })

@app.route('/learningDatas/<classID>', methods=['GET'])
def getLearningDatasOfClassID(classID) : #ClassID에 따른 LearingID 가져오기
  if request.method == 'GET' :
    #임시 : classID와 관련 없이 모두 get
    flag = True
    LearningDatas = Learning.AllData()
    
    return  jsonify (
      {
        "success" : flag,
        "data" : LearningDatas,
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

  CORS(app)

  app.run(port="5001", debug=False)  # host 등을 직접 지정하고 싶다면 app.run(host="127.0.0.1", port="5000", debug=True)
