import time
import requests
import json
from requests.api import head, options
from requests.models import Response
import websocket
import threading
from dhooks import Embed, Webhook
import datetime
import jwt
import os
import random
from urllib.parse import quote
import logging

cd = os.path.dirname(os.path.realpath(__file__))

embedColor = 0xFF6347

#mainControllerToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYwMjkzMzM5MGU0NWNiOTEyZmJkOGJlMCIsIm1vYmlsZSI6Ijk2Njk3MDkxNzkiLCJmaXJzdE5hbWUiOiI5NioqKio5MTc5Iiwic291cmNlIjoiU3lGUU52SUNEYyIsImlhdCI6MTYxMzU3MTY2OH0.o5H8y8vE0vmhmlEnCJo2OGExj_VlzZlHZ6umcBL5L4M" #966
#mainControllerToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYwMWUzZDg4NzE3NWEzYzM0YzIxZWM5OSIsIm1vYmlsZSI6IjkzMDEyNzEyMTAiLCJmaXJzdE5hbWUiOiI5MyoqKioxMjEwIiwic291cmNlIjoiU3lGUU52SUNEYyIsImlhdCI6MTYxMjU5NDU4N30.MUPWC1mIl6tmodS1Yk4DPpBkNI1WpwXVMoszFw7HuAw"
mainControllerToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYwMWU3MDM1YzA1ZmNlYzI5ZmQwNTIzNSIsIm1vYmlsZSI6IjcwMjQ4ODU3OTIiLCJmaXJzdE5hbWUiOiI3MCoqKio1NzkyIiwic291cmNlIjoiU3lGUU52SUNEYyIsImlhdCI6MTYxMzU3NTQ4Mn0.9sPqDbQbcZiJO73dQ4bwyu3M7cBKNP4d_JK2IPdswSo"

tokens = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYwMWUzOWYxMTI0YmI3YTliOGYwMTNjMSIsIm1vYmlsZSI6Ijk4MjYxNDEyMDciLCJmaXJzdE5hbWUiOiI5OCoqKioxMjA3Iiwic291cmNlIjoiU3lGUU52SUNEYyIsImlhdCI6MTYxMzY1Nzg3OX0.DjMDly3Y1JFqjoLwKuW2JF0j28Kjd44xol9eF6J0F7M", #9826141207
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYwMWUzZDg4NzE3NWEzYzM0YzIxZWM5OSIsIm1vYmlsZSI6IjkzMDEyNzEyMTAiLCJmaXJzdE5hbWUiOiJzdW1hbiIsInNvdXJjZSI6IlN5RlFOdklDRGMiLCJpYXQiOjE2MTM2NTc5NjJ9.9caa7JwbrpfZFK95AXskdmDAouh6cPBJUxntjrI9WgU", #9301271210
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYwMzA3MmIwZDhhMmQ2OTM0YjA2YWUxMCIsIm1vYmlsZSI6Ijg0MzUzNTkwNTYiLCJmaXJzdE5hbWUiOiI4NCoqKio5MDU2Iiwic291cmNlIjoiU3lGUU52SUNEYyIsImlhdCI6MTYxMzc4NzkyNn0.JJzSLkTJPZ05uOKh_KMhiEnSgEr4UtGmsRDwRXXhGr8", #papa
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYwMzBhYWNmMGU0NWNiOTEyZmJlYWNlMyIsIm1vYmlsZSI6IjkzMDIzMTk5NTYiLCJmaXJzdE5hbWUiOiI5MyoqKio5OTU2Iiwic291cmNlIjoiU3lGUU52SUNEYyIsImlhdCI6MTYxMzgwMjI3OH0.dXzv7jdP_QlP9zadAqMdQudhj5xDIo5ZT7xRwaQpiHE", #shanu 2
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYwMWU3MDM1YzA1ZmNlYzI5ZmQwNTIzNSIsIm1vYmlsZSI6IjcwMjQ4ODU3OTIiLCJmaXJzdE5hbWUiOiI3MCoqKio1NzkyIiwic291cmNlIjoiU3lGUU52SUNEYyIsImlhdCI6MTYxMzU3NTQ4Mn0.9sPqDbQbcZiJO73dQ4bwyu3M7cBKNP4d_JK2IPdswSo", #akash1
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYwMmZiZTAzZDhhMmQ2OTM0YjA2OTFmNSIsIm1vYmlsZSI6Ijc5NzQ4ODkwNzMiLCJmaXJzdE5hbWUiOiI3OSoqKio5MDczIiwic291cmNlIjoiU3lGUU52SUNEYyIsImlhdCI6MTYxMzc0MTc4OH0.RGZ_WqLlQi2HK-mSnmbcWQck4IUGbBimuu6gLJ3LHVU", #akash2
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYwMjhiYjEyZjhmNTM5NDUyMzE3ZTYxNiIsIm1vYmlsZSI6IjgwNzcyMTMyMDUiLCJmaXJzdE5hbWUiOiJBbml0YSIsInNvdXJjZSI6IlN5RlFOdklDRGMiLCJpYXQiOjE2MTM2NTgzMDl9.7uafdpmnNcEU16PeCYqrMCJVL3yN6XLpZtenxuERkX4", #gabru 1
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYwMWU0OTc5MjdiMTE5ZjQ5M2ZiOGEyOCIsIm1vYmlsZSI6Ijk3NzM4MzM5NzIiLCJmaXJzdE5hbWUiOiJBREgzM1JBIiwic291cmNlIjoiU3lGUU52SUNEYyIsImlhdCI6MTYxMzY1ODY1MX0.AWq5sIWvDDwqnCveVI7jmt6O0B0nAll0xhoyPKFROoY", #gabru 2
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYwMzAwOWEyZjhmNTM5NDUyMzE5MDU3NyIsIm1vYmlsZSI6IjkxNzQxNzIyNjciLCJmaXJzdE5hbWUiOiI5MSoqKioyMjY3Iiwic291cmNlIjoiU3lGUU52SUNEYyIsImlhdCI6MTYxMzc2MTAxMH0.bwZfxelNM6DwYFtMnYmpKQJ-BviZCTGTnCvxdXbXd4I", #shanu 1
)
#===========================================================

webhook = Webhook("https://discord.com/api/webhooks/792751034501038101/qzaAmoXwsetfIDDpdQe3TDDqRPzxBmUxC3uX_ycTcqpmmR0Y2P5tfNeccD9XeU2JCBxc")

class MainControllerAlreadyExistsError(Exception):
    pass

class Emulator:
    counts = 0
    mainController = None
    def __init__(self,authToken=None,isMain=False,isFriend=False,canWrong=0):
        if Emulator.mainController:
            if isMain:
                raise MainControllerAlreadyExistsError
        self.verify = True
        self.authToken = authToken
        self.eventId = None
        self.sessionId = None
        self.cookies = None
        self.agoraId = None
        self.pingInterval = 0
        self.pingTimeout = 0
        self.isMain = isMain
        self.isFriend = isFriend
        self.wrongAnswerCount = 0
        self.submitedAnswers = 0
        self.canWrongRemaining = canWrong
        self.totalCanWrong = canWrong
        if self.isMain is True:
            Emulator.mainController = self
        if self.authToken != None:
            Emulator.counts+=1
            self.Id = Emulator.counts
            userInfo = jwt.decode(self.authToken, options={"verify_signature": False},algorithms=["HS256"])
            self.number = userInfo['mobile']
            self.firstName = userInfo['firstName']
            self.userId = userInfo['id']
        self.ws = None
        self.winPrize = 0
        self.winnerDetails = {}
        self.questions = {}
    def __str__(self):
        js = {f"emulatorId":self.Id,"number":self.number,"name":self.firstName,"userId":self.userId,"isMain":self.isMain}
        return json.dumps(js)

    def getEvents(self):
        url = "https://api.fangame.live/event/getEvents?page=undefined"
        headers = {"user-agent": "okhttp/3.12.12","accept": "application/json, text/plain, */*","accept-encoding": "gzip","x-source-app": "SyFQNvICDc"}
        response = requests.get(url,headers=headers,verify=self.verify).json()
        return response.get("upcomingEvents")

    def getLatestEvent(self):
        return self.getEvents()[0]

    def getEventDetails(self,eventId):
        url = f"https://api.fangame.live/event/getEventDetails?eventId={eventId}"
        headers = {"user-agent": "okhttp/3.12.12","accept": "application/json, text/plain, */*","accept-encoding": "gzip","x-source-app": "SyFQNvICDc"}
        response = requests.get(url,headers=headers,verify=self.verify).json()
        return response
    def getAgoraTempToken(self,eventId):
        url = f"https://api.fangame.live/user/getAgoraTokenTEMP?eventId={eventId}"
        headers = {"user-agent": "okhttp/3.12.12","accept": "application/json, text/plain, */*","accept-encoding": "gzip","x-auth-token":self.authToken}
        response = requests.get(url,headers=headers,verify=self.verify).json()
        return response
    
    def getAgoraRTMToken(self,eventId):
        url = f"https://api.fangame.live/user/getAgoraRTMTokenTEMP?eventId={self.eventId}"
        headers = {"user-agent": "okhttp/3.12.12","accept": "application/json, text/plain, */*","accept-encoding": "gzip","x-auth-token":self.authToken}
        response = requests.get(url,headers=headers,verify=self.verify).json()
        return response

    def setEventId(self,eventId)->None:
        self.eventId = eventId

    def registerForEvent(self,eventId):
        url = "https://api.fangame.live/event/registerForEvent"
        payload = {"eventId": self.eventId}
        headers = {"user-agent": "okhttp/3.12.12","accept": "application/json, text/plain, */*","accept-encoding": "gzip","x-auth-token":self.authToken,"content-type": "application/json","content-length": "38"}
        response = requests.post(url,headers=headers,json=payload,verify=self.verify).json()
        print(f"Emulator id {self.Id}: {response}")
        return response
    
    def user_authanticate(self,socketId,eventId,secretId=None):
        url = "https://api.fangame.live/pusher/user-authenticate"
        
        if not secretId:
            payload = f"socket_id={socketId}&channel_name=private-{eventId}"
        else:
            payload = f"socket_id={socketId}&channel_name=private-{eventId}-{secretId}"
        headers = {"x-auth-token": self.authToken,
        "content-type": "application/x-www-form-urlencoded",
        "content-length": str(len(payload)),
        "accept-encoding": "gzip",
        
        "user-agent": "okhttp/3.12.12"}
        response = requests.post(url,headers=headers,data=payload,verify=self.verify).json()
        return response['auth']
        
    
    def joinEvent(self,eventId,socketId):
        url = "https://api.fangame.live/pusher/join-event"
        headers = {"accept": "application/json, text/plain, */*",
        "x-auth-token": self.authToken,
        "content-type": "application/json;charset=utf-8",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/3.12.12"}
        payload = {"eventId":eventId,"socketId":socketId}
        response = requests.post(url,headers=headers,json=payload,verify=self.verify).json()
        secretEventId = response['agoraChannelToken']['id']
        self.agoraId = response['agoraChannelToken']['id']
        return secretEventId

    def getLeaks(self,eventId,countNumber=1):
        currentQuestionNumber = self.questions.get("questionNumber")
        events = self.getEvents()
        for event in events:
            if event['_id'] == self.eventId:
                lastQuestionDetails = event['lastQuestionDetails']
                questionNumber = lastQuestionDetails['number']
                if questionNumber==0:
                    return
                if currentQuestionNumber!= questionNumber and questionNumber!=0:
                    if countNumber>5:
                        return
                    time.sleep(1)
                    self.getLeaks(eventId,countNumber+1)
                    return
                question = lastQuestionDetails['question']
                options = lastQuestionDetails['options']
                correctAnswerOption = lastQuestionDetails['answer']
                embed = Embed(title=f"{question}")
                correctAnswer = options[correctAnswerOption-1]
                print(f"Correct Answer:\n{correctAnswerOption}) {correctAnswer}")
                embed.add_field(name="Correct Answer:",value=f"{correctAnswerOption}) {correctAnswer}")
                
                return correctAnswerOption , lastQuestionDetails['qid'], embed

    def submitAnswer(self,qid,correct):
        if self.submitedAnswers > 1:
            seconds = 9
        else:
            seconds = 8
            self.submitedAnswers += 2
        url = "https://api.fangame.live/pusher/submit-answer"
        headers = {"content-type": "application/json",
        "content-length": "193",
        "accept-encoding": "gzip",
        "x-auth-token":self.authToken,
        "user-agent": "okhttp/3.12.12"}
        payload = {"answer":{"qid":qid,"option":correct,"seconds":seconds},"eventId":self.eventId,"user":{"id":self.userId,"mobile":self.number,"firstName":self.firstName,"source": "SyFQNvICDc"}}
        response = requests.post(url,headers=headers,json=payload).json()
        msg= f"Emulator Id {self.Id}: Submitted Answer! || [{response}]"
        print(msg)

    def submitAnswerFake(self,qid,correct):
        if self.submitedAnswers > 1:
            seconds = 9
        else:
            seconds = 8
            self.submitedAnswers += 2
        if self.canWrongRemaining>0 and self.totalCanWrong<=10:
            seconds = seconds - 1
            self.canWrongRemaining = self.canWrongRemaining - 1
        elif self.canWrongRemaining>0:
            seconds = seconds - 1 - 1*(self.totalCanWrong//10)
            self.canWrongRemaining = self.canWrongRemaining - 1
        url = "https://api.fangame.live/pusher/submit-answer"
        headers = {"content-type": "application/json",
        "content-length": "193",
        "accept-encoding": "gzip",
        "x-auth-token":self.authToken,
        "user-agent": "okhttp/3.12.12"}
        payload = {"answer":{"qid":qid,"option":correct,"seconds":seconds},"eventId":self.eventId,"user":{"id":self.userId,"mobile":self.number,"firstName":self.firstName,"source": "SyFQNvICDc"}}
        response = requests.post(url,headers=headers,json=payload).json()
        msg= f"Emulator Id {self.Id}: Submitted Answer! || [{response}]"
        print(msg)


    def getLeaderboard(self,eventId):
        url = f"https://api.fangame.live/pusher/{eventId}/leader-board?"
        headers = {"accept":"application/json, text/plain, */*","user-agent":"okhttp/3.12.12","cookie": self.cookies,"x-auth-token":self.authToken}
        response =  requests.get(url,headers=headers,verify=self.verify).json()
        if response['msg'] == "Please try after sometime":
            time.sleep(20)
            return self.getLeaderboard(eventId)
        return response['leaderBoard']

    def getTransactionHistory(self,eventId=None):
        url = f"https://api.fangame.live/user/transactionHistory?"
        headers = {"accept":"application/json, text/plain, */*","user-agent":"okhttp/3.12.12","x-auth-token":self.authToken}
        response = requests.get(url,headers=headers).json()
        if eventId is not None:
            transactions = response['transactions']
            for transaction in transactions:
                if transaction.get("eventId") == eventId:
                    return transaction
            return None
        return response
    def connect(self):
        self.getAgoraTempToken(self.eventId)
        self.getAgoraRTMToken(self.eventId)
        self.registerForEvent(self.eventId)
        def on_open(ws):
            if self.isMain is True:
                msg = "Main Controller Connected!"
                print(msg)
            else:
                msg = f"Emulator Account Id {self.Id} Connected!"
                print(msg)
        def on_error(ws,error):
            msg = f"Emulator Id {self.Id} error: {str(error)}"
            print(msg)
        def on_close(ws):
            msg = f"Emulator Id {self.Id}: Connection Closed!"
            print(msg)
        #=================================
        def on_message(ws,message):
            print(message)
            message = json.loads(message)
            data = json.loads(message['data'])
            eventType = message['event']
            if eventType == "pusher:connection_established":
                socketId = data['socket_id']
                auth1 = self.user_authanticate(socketId,self.eventId)
                js = {"event":"pusher:subscribe","data":{"auth":auth1,"channel":f"private-{self.eventId}"}}
                self.ws.send(json.dumps(js,separators = (",", ":")))
                
                auth2 = self.user_authanticate(socketId,self.eventId,self.userId)
                js = {"event":"pusher:subscribe","data":{"auth":auth2,"channel":f"private-{self.eventId}-{self.userId}"}}
                self.ws.send(json.dumps(js,separators = (",", ":")))
                self.joinEvent(self.eventId,socketId)
                #=================================================
            if self.isMain is False:
                return
            if message.get("event") == "newQuestion":
                qid = data["qid"]
                questionNumber = data['number']
                question = data['question']
                self.questions['question'] = question
                self.questions['qid'] = qid
                googlelink = f"https://google.com/search?q="
                googleWOAnswers = googlelink+quote(question)
                embed = Embed(title=f"{question}",url=googleWOAnswers,color=embedColor)
                #webhook.send(embed=embed)
                self.questions['questionNumber'] = questionNumber
            if message.get("event") == "options":
                options = data
                self.questions['options'] = options
                question = self.questions['question']
                qid = self.questions['qid']
                embed = Embed(title=f"{question}",color=embedColor)
                optionNumber = 1
                for option in options:
                    embed.add_field(name=f"Option {optionNumber}:",value=f"{option}",inline=False)
                    optionNumber+=1
                #webhook.send(embed=embed)
                try:
                    correct,qid ,embed= self.getLeaks(self.eventId)
                    self.submitAnswer(qid,correct)
                    [threading.Thread(target = emu.submitAnswer, args = [qid, correct]).start() for emu in emus]
                    #for emu in emus:
                    #    threading.Thread(target = emu.submitAnswer, args = [qid, correct]).start()
                    #self.getLeaks(self.eventId)
                    webhook.send(embed=embed)
                except Exception as e:
                    print(e)
            if message.get("event") == "totalScores":
                totalScores = self.getLeaderboard(self.eventId)
                with open(f"{cd}\{datetime.datetime.now().date()} {self.eventId}.json","w+") as f:
                    json.dump(totalScores,f)
                print("successfully dumped today's winner details")
                ws.close()
                for emu in emus:
                    threading.Thread(target = emu.ws.close).start()



        
        #=================================
        url = "wss://ws-ap2.pusher.com/app/7c0e1751e3e734fc0273?protocol=7&client=js&version=7.0.2&flash=false"
        self.ws = websocket.WebSocketApp(url,on_message = on_message,on_error = on_error,on_close = on_close)
        self.ws.on_open = on_open
        self.ws.run_forever()


emus = [Emulator(token) for token in tokens]

def start(eventId):
    for emu in emus:
        emu.setEventId(eventId)
    threads = [threading.Thread(target=emu.connect) for emu in emus]
    for thread in threads:
        thread.start()

if __name__ == "__main__":
    
    event = Emulator().getLatestEvent()
    eventId = event.get("_id")
    eventName = event['eventName']
    mainController = Emulator(mainControllerToken,isMain=True)
    print(mainController)
    for emu in emus:
        print(emu)
    exit()
    mainController.setEventId(eventId)
    mainThread = threading.Thread(target=mainController.connect)
    mainThread.start()
    exit()
    print(mainController)
    start(eventId)
    for emu in emus:
        print(emu)

    
