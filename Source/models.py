from collections import UserDict
import firebase_admin
from firebase_admin import credentials, storage
from firebase_admin import db
from uuid import uuid4

#데이터베이스
cred = credentials.Certificate("key\hello-python-fbe83-firebase-adminsdk-4updc-c46193ba98.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://hello-python-fbe83-default-rtdb.firebaseio.com/',
    'storageBucket': 'hello-python-fbe83.appspot.com'
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
                'point' : 0,
                'profileImage' : 'https://firebasestorage.googleapis.com/v0/b/hello-python-fbe83.appspot.com/o/user.png?alt=media&token=6b8057b2-5e01-4874-95dd-34406afc1c34',
            })
            return True
        except Exception as e:
            print(e)
            return False
        return False
    
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
                for key, value in userPath.items() :
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
    
    def LogoutData() :
       userData = '' #데이터 초기화

    def GetUserData(userid) :
        try :
            userPath = db.reference('/Users').get()
            if (userPath) : 
                for key, value in userPath.items() :
                    if key == userid : 
                        return value
        except Exception as e:
            print(e)
        return None
    
    def SetProfileImage(userid, filepath) :        
        bucket = storage.bucket()
        blob = bucket.blob(filepath)

        # Create new token
        new_token = uuid4()
        # Create new dictionary with the metadata
        metadata  = {"firebaseStorageDownloadTokens": new_token}
        blob.metadata = metadata

        # Upload file
        blob.upload_from_filename(filename=filepath, content_type='image/png')
        blob.make_public()

        # delete origin File


        # change path
        db.reference('/Users').child(userid).update({
            'profileImage' : blob.public_url,
        })



