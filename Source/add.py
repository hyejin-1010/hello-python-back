import os #디렉토리 절대 경로
from flask import Flask
from flask import render_template #template폴더 안에 파일을 쓰겠다
from flask import request #회원정보를 제출할 때 쓰는 request, post요청 처리
from flask import redirect #리다이렉트
from flask import session #세션
from flask_wtf.csrf import CSRFProtect #csrf
app = Flask(__name__)

#다른 .py 임포트
from models import User
from forms import RegisterForm, LoginForm

@app.route('/') # 테스트 url
def mainpage():
  userid = session.get('userid',None)
  return render_template('main.html', userid=userid)

@app.route('/register/', methods=['GET','POST']) #회원가입
def register() :
  form = RegisterForm()
  if form.validate_on_submit(): 
    userid = request.form.get('userid')
    nickname = request.form.get('nickname')
    password = request.form.get('password')

    if User.RegisterData(userid, nickname, password) :
      return redirect('/') #성공하면 main.html로
    else :
      return "중복된 아이디입니다."
    
  return render_template("register.html", form=form)

@app.route('/deleteUser/', methods=['GET','POST']) #삭제
def deleteUser() :
  User.DeleteData(session['userid'])
  return redirect('/')

def do_the_login(args) :
  return { 'success': True }

@app.route('/login/', methods=['GET','POST']) #login
def login(args) :
  print('call login')
  if request.method == 'POST':
    return do_the_login(args)
  else:
    form = LoginForm() #로그인폼
    if form.validate_on_submit(): #유효성 검사
      print('{}가 로그인 했습니다'.format(form.data.get('userid')))
      session['userid']=form.data.get('userid') #form에서 가져온 userid를 세션에 저장
      return redirect('/') #성공하면 main.html로
    return render_template('login.html', form=form)

@app.route('/logout/', methods=['GET']) 
def logout() : 
  session.pop('userid', None)
  return redirect('/')

if __name__=="__main__":

  # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
  app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True #사용자에게 정보 전달완료하면 teadown. 그 때마다 커밋=DB반영
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #추가 메모리를 사용하므로 꺼둔다
  app.config['SECRET_KEY']='asdfasdfasdfqwerty' #해시값은 임의로 적음

  '''
  csrf = CSRFProtect()
  csrf.init_app(app)
  '''

  app.run(debug=False)  # host 등을 직접 지정하고 싶다면 app.run(host="127.0.0.1", port="5000", debug=True)
