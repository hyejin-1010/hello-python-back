from collections import UserDict
import firebase_admin
from firebase_admin import credentials, storage
from firebase_admin import db
from flask import jsonify #jsonify
from uuid import uuid4

#데이터베이스
cred = credentials.Certificate("key\hello-python-fbe83-firebase-adminsdk-4updc-c46193ba98.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://hello-python-fbe83-default-rtdb.firebaseio.com/',
    'storageBucket': 'hello-python-fbe83.appspot.com'
})
dir = db.reference() #기본 위치 지정

class User(): #사용자 정보
    def __init__(self) :
        self.userid = 'userid'
        self.nickname = 'nickname'
        self.password = 'password'
        self.point = 0
        self.profileImage = 'https://firebasestorage.googleapis.com/v0/b/hello-python-fbe83.appspot.com/o/user.png?alt=media&token=6b8057b2-5e01-4874-95dd-34406afc1c34'
        self.completedLearnings = [] #lerning 완료된 uid 저장 배열

    def changeData(value) : 
        data = {
            "userid" : value.get('userid'),
            "nickname" : value.get('nickname'),
            "password" : value.get('password'),
            "point" : value.get('point'),
            "profileImage" : value.get('profileImage'),
            "completedLearnings" : [] if value.get('completedLearnings') is None else list(value.get('completedLearnings').values()),
        }
        return data
    
    def RegisterData(userid, nickname, password) :
        try :
            userPath = db.reference('/Users').get()
            # DB에서 아이디 중복 확인 한번 더 확인

            if (userPath) : 
                for key, value in userPath.items() :
                    if str(value['userid']) == str(userid) :
                        return False

            #중복 값이 아니면 아이디 저장
            userPath = db.reference('/Users')
            userPath.child(userid).set({
                'userid' : userid,
                'nickname' : nickname,
                'password' : password,
                'point' : 0,
                'profileImage' : 'https://firebasestorage.googleapis.com/v0/b/hello-python-fbe83.appspot.com/o/user.png?alt=media&token=6b8057b2-5e01-4874-95dd-34406afc1c34',
                'completedLearnings' : []
            })
            return True
        except Exception as e:
            print(e)
            return False
    
    def RegisterDoubleCheck(userid) :
        # DB에서 아이디 중복 확인해서 상태 리턴
        userPath = db.reference('/Users').get()

        if (userPath) : 
            for key, value in userPath.items() :
                if str(value['userid']) == str(userid) :
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
                for key, value in userPath.items() :
                    if str(value['userid']) == str(userid) :
                        if value['password'] == password :
                            return True
                        else :
                            return False #비밀번호가 일치하지 않습니다.
                return False #일치하는 아이디가 없습니다.
        except Exception as e:
            print(e)
            return False
        return True
    
    def GetUserData(userid) :
        try :
            userPath = db.reference('/Users').get()
            if (userPath) : 
                for key, value in userPath.items() :
                    if str(value['userid']) == str(userid) :
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
        # tempData = db.reference('/Users').child(userid).get()
        # temp = bucket.get_blob() (tempData['profileImage'])
        # temp.delete()

        # change path
        db.reference('/Users').child(userid).update({
            'profileImage' : blob.public_url,
        })
    
    def addCompleteData(userid, learningID) : 
        try : 
            userData = User.GetUserData(userid)
            if learningID not in userData['completedLearnings'].values() : 
                db.reference('/Users').child(userid).child('completedLearnings').push(learningID)
            
            originPoint = int(userData['point'])
            earnPoint = int(Learning.getPointData(learningID))
            db.reference('/Users').child(userid).update({
                'point' : originPoint+earnPoint
                })
            return True
        except Exception as e:
            print(e)
            return False
    
    def GetRanking() : 
        userPath = db.reference('/Users').get()
        ranking = []
        if (userPath) : 
            for key, value in userPath.items() :
                ranking.append(
                    {'nickname' : value['nickname'], 
                     'point' :  value['point']})

            rr = sorted(ranking, key=(lambda x : x['point']), reverse=True) #sort
            return rr
        return None     
    
    def IsAdmin(userid) :
        try : 
            userData = User.GetUserData(userid)
            if userData is not None : 
                if userData.get('role') == "admin" :
                    return True 

        except Exception as e:
            print(e)
        return False

class Lesson : #DB는 class인데 예약어라 사용 불가능하여 수정 
    pass

class Learning :    
    def __init__(self) :
        self.learningID = 0
        self.Title = "n번째 강의입니다."
        self.video = "url" # 강의 영상 url
        self.pointGameIDs = ["111","222"] # pointGame 데이터베이스 정보
        
    def getData(self) : 
        data = {
            "learningID" : self.learningID,
            "Title" : self.Title,
            "video" : self.video,
            "pointGameIDs" : self.pointGameIDs,
        }
        return data
    
    def addLearning(self) :
        try :
            #path = db.reference('/Learning').get()

            if Learning.findLearningData(self.learningID) != None :  #중복 uid 
                return False

            #정보 저장
            userPath = db.reference('/Learning')
            userPath.child(self.learningID).set({ 
                'learningID' : self.learningID,
                'Title' : self.Title,
                'video' : self.video,
                'pointGameIDs' : self.pointGameIDs,
            })

            return True
        except Exception as e:
            print(e)
            return False

    def editLearning(self) :
        try :
            if Learning.findLearningData(self.learningID) == None :  #정보 없음 
                return False

            #정보 저장
            userPath = db.reference('/Learning')
            userPath.child(self.learningID).update({ 
                'learningID' : self.learningID,
                'Title' : self.Title,
                'video' : self.video,
                'pointGameIDs' : self.pointGameIDs,
            })
            return True
        except Exception as e:
            print(e)
            return False
            
    def deleteLearning(learningID) :
        try :
            if Learning.findLearningData(learningID) == None :  #정보 없음 
                return False

            db.reference('/Learning/' + learningID).delete()
            return True
        except Exception as e:
            print(e)
            return False

    def findLearningData(learningID) : 
        userPath = db.reference('/Learning').get()
        if (userPath) : 
            for key, value in userPath.items() :
                if str(value['learningID']) == str(learningID) :
                    return value
        return None #일치하는 정보 없음
    
    def AllData() :
        userPath = db.reference('/Learning').get()
        if (userPath) :
            data = {}
            for key, value in userPath.items() : 
                data[key] = value
            return data
        return None

    def getPointData(learningID) :  #LearningID와 연관된 모든 earnPoint값을 가져온다.
        allPoint = 0
        try :
            data = Learning.findLearningData(learningID)
            if data == None :  #정보 없음 
                return allPoint
                
            for pointgameID in data['pointGameIDs'] : 
                ptData = PointGame.finePointGame(pointgameID)
                if ptData != None : 
                    allPoint += int(ptData['earnPoint'])
            return allPoint
        except Exception as e:
            print(e)
            return allPoint
 
class PointGame : 
    def __init__(self) :
        self.pointGameID = 0
        self.title = "타이틀"
        self.description = "설명"
        self.content = "내용"
        self.answer = "corectAnswer"
        self.selection  = {
            "예제1":"a",
            "예제2":"b",
            "예제3":"c"
        } #객관식의 경우 예시
        self.hint = {
            "1" : "내용",
            "2" : "내용",
            "3" : "내용"
        }
        self.earnPoint = 5  #정답을 맞추면 벌 수 있는 포인트. 힌트 사용시 n점씩 줄어든다.
    
    def getData(self) :
        data = {
            "pointGameID" : self.pointGameID,
            "title" : self.title,
            "description" : self.description,
            "content" : self.content,
            "answer" : self.answer,
            "selection" : self.selection,
            "hint" : self.hint,
            "earnPoint" : self.earnPoint ,
        }
        return data

    def addPointGame(self) : 
        try :
            if PointGame.finePointGame(self.pointGameID) != None :  #중복 uid 
                return False

            #정보 저장
            userPath = db.reference('/PointGame')
            userPath.child(self.pointGameID).set({ 
                'pointGameID' : self.pointGameID,
                "title" : self.title,
                "description" : self.description,
                "content" : self.content,
                "answer" : self.answer,
                "selection" : self.selection,
                "hint" : self.hint,
                "earnPoint" : self.earnPoint ,
            })
            return True
        except Exception as e:
            print(e)
            return False

    def editPointGame(self) : 
        try :
            if PointGame.finePointGame(self.pointGameID) == None :  #정보 없음 
                return False

            #정보 저장
            userPath = db.reference('/PointGame')
            userPath.child(self.pointGameID).update({ 
                "pointGameID" : self.pointGameID,
                "title" : self.title,
                "description" : self.description,
                "content" : self.content,
                "answer" : self.answer,
                "selection" : self.selection,
                "hint" : self.hint,
                "earnPoint" : self.earnPoint ,
            })
            return True
        except Exception as e:
            print(e)
            return False

    def deletePointGame(pointGameID) : 
        try :
            if PointGame.finePointGame(pointGameID) == None :  #정보 없음 
                return False

            db.reference('/PointGame/' + pointGameID).delete()
            return True
        except Exception as e:
            print(e)
            return False

    def finePointGame(pointGameID) : 
        userPath = db.reference('/PointGame').get()
        if (userPath) : 
            for key, value in userPath.items() :
                if str(value['pointGameID']) == str(pointGameID) :
                    return value
        return None #일치하는 정보 없음

    def AllData() :
        userPath = db.reference('/PointGame').get()
        if (userPath) :
            data = {}
            for key, value in userPath.items() : 
                data[key] = value
            return data
        return None

class Dice : 
    def __init__(self) :
        self.diceID = 0
        self.pointGameIDs = ["111","222"] # pointGame 데이터베이스 정보
    
    def getData(self) :
        data = {
            "diceID" : self.diceID,
            "pointGameIDs" : self.pointGameIDs,
        }
        return data

    def addDice(self) : 
        try :
            if Dice.findDice(self.diceID) != None :  #중복 uid 
                return False

            #정보 저장
            userPath = db.reference('/Dice')
            userPath.child(self.diceID).set({ 
                'diceID' : self.diceID,
                "pointGameIDs" : self.pointGameIDs,
            })
            return True
        except Exception as e:
            print(e)
            return False

    def editDice(self) : 
        try :
            if Dice.findDice(self.diceID) == None :  #정보 없음 
                return False

            #정보 저장
            userPath = db.reference('/Dice')
            userPath.child(self.diceID).update({ 
                "diceID" : self.diceID,
                "pointGameIDs" : self.pointGameIDs,
            })
            return True
        except Exception as e:
            print(e)
            return False

    def deleteDice(diceID) : 
        try :
            if Dice.findDice(diceID) == None :  #정보 없음 
                return False

            db.reference('/Dice/' + diceID).delete()
            return True
        except Exception as e:
            print(e)
            return False

    def findDice(diceID) : 
        userPath = db.reference('/Dice').get()
        if (userPath) : 
            for key, value in userPath.items() :
                if str(value['diceID']) == str(diceID):
                    return value
        return None #일치하는 정보 없음

    def AllData() :
        userPath = db.reference('/Dice').get()
        if (userPath) :
            data = {}
            for key, value in userPath.items() : 
                data[key] = value
            return data
        return None

        


