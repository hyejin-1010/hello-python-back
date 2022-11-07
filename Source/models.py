from collections import UserDict
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#데이터베이스
cred = credentials.Certificate("hello-python-fbe83-firebase-adminsdk-4updc-c46193ba98.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://hello-python-fbe83-default-rtdb.firebaseio.com/'
})
dir = db.reference() #기본 위치 지정

class User(): #사용자 정보
    def __init__() : pass

    def RegisterData(userid, nickname, password) :
        try :
            userPath = db.reference('/Users').get()
            # DB에서 아이디 중복 확인해서 상태 리턴

            if (userPath) : 
                for key in userPath.items() :
                    if key == userid :
                        return False

            #중복 값이 아니면 아이디 저장
            userPath = db.reference('/Users')
            userPath.child(userid).set({
                'userid' : userid,
                'nickname' : nickname,
                'password' : password,
            })
        except Exception as e:
            print(e)
            return False
        return True
    
    def DeleteData(userid) :
        try :
            userPath = db.reference('/Users/' + userid).get()
            if (userPath) : 
                db.reference('/Users/' + userid).delete()
                return True
            else :
                return False
        except Exception as e:
            print(e)
            return False

    def LoginData(userid, password) :
        try :
            userPath = db.reference('/Users').get()
            if (userPath) : 
                for key ,value in userPath.items() :
                    if key == userid : 
                        if value['password'] == password :
                            return True
                        else :
                            return False #비밀번호가 일치하지 않습니다.
                return False #일치하는 아이디가 없습니다.
        except Exception as e:
            print(e)
            return False
        return True
        

