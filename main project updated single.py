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

mainControllerToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZjA4MGM3Y2YzNTNjY2U0NGI3ODdhOCIsIm1vYmlsZSI6Ijk2Njk3MDkxNzkiLCJmaXJzdE5hbWUiOiI5NioqKio5MTc5IiwiaWF0IjoxNjA5NjA4ODQ5fQ.Gv9VE8WXlMjoZz0Mt-C-tMchegxALx4Gv1WQ5Cg5mnk" #mummy 

tokens = (
    #"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZjVjODc0ZTE1MjQxMWJkYzg3MTE1NyIsIm1vYmlsZSI6Ijg1MjA4MzM5MDkiLCJmaXJzdE5hbWUiOiI4NSoqKiozOTA5IiwiaWF0IjoxNjEzNjU4NDgzfQ.1JNONnI7915zvDO-E7LpXhC4Fix4g0gbgtIe5vNgPLg",
     "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTg5OTg1ZjA2YTFmNTJkMDY3YTc1NSIsIm1vYmlsZSI6IjkzMDEyNzEyMTAiLCJmaXJzdE5hbWUiOiI5MyoqKioxMjEwIiwiaWF0IjoxNjA5NTk2ODU0fQ.gMr3kFsRwiRD_Mx88BYKT1YauUwhQkYUP4Q9Vc-651M", #9301271210
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTg4ZDEyZjA2YTFmNTJkMDY3OWUwYyIsIm1vYmlsZSI6Ijk4MjYxNDEyMDciLCJmaXJzdE5hbWUiOiJhbWl0IiwiaWF0IjoxNjA5OTE5MjY0fQ.ywUzJruJncXW47qs0xmg5AiZxk95ajqH3UaybbinHz0", #main number
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZjA5Y2FiY2YzNTNjY2U0NGI3OGVkMCIsIm1vYmlsZSI6Ijg0MzUzNTkwNTYiLCJmaXJzdE5hbWUiOiJBc2hvayBHdXB0YSIsImlhdCI6MTYwOTYxNDc3OX0.NV2IFAfr3HmeIcLYoABT7siRC8_z1-SlVACOhIiEdww", #ashok
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTVhNDU3MzQ4N2ExNzZlMmI3ZGI5ZSIsIm1vYmlsZSI6Ijk3NzM4MzM5NzIiLCJmaXJzdE5hbWUiOiJQcmluY2UiLCJpYXQiOjE2MDk4NTI4OTB9.k0hXVINO3TfCH3gXbGLF4Eei_kPgFfoTLsT_bE-IMAk", #abhi-1
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTg5OTI1ZjA2YTFmNTJkMDY3YTcxZSIsIm1vYmlsZSI6IjgwNzcyMTMyMDUiLCJmaXJzdE5hbWUiOiJBYmhpIiwiaWF0IjoxNjA5ODUzMTM0fQ.pRTnxvqEjvhVElbY3HPdoFS3A1OrPUUwnTooOe8biYA", #abhi 2
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZjFlMmIyY2YzNTNjY2U0NGI3OWRkYyIsIm1vYmlsZSI6Ijk3NTM3OTIzNDkiLCJmaXJzdE5hbWUiOiI5NyoqKioyMzQ5IiwiaWF0IjoxNjA5ODM2MTk0fQ.MopqRg1hd5jEnsbuOSaP_aEkwQzN5i4Rp_59R2ZeJRQ", #akash 1
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTg5MGE0ZjA2YTFmNTJkMDY3OWVhZCIsIm1vYmlsZSI6IjcwMjQ4ODU3OTIiLCJmaXJzdE5hbWUiOiJDYXNhbm92YSIsImlhdCI6MTYwOTg1OTI0NH0._vKI7rDHJCNIfmz9WVQ6g6jk7Sbg4wjLHXYBE7lme60", #akash 2
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYwM2M1MDViZDhhMmQ2OTM0YjA4NDJjMSIsIm1vYmlsZSI6Ijk0MDY5MTQ3NjgiLCJmaXJzdE5hbWUiOiI5NCoqKio0NzY4IiwiaWF0IjoxNjE0NTY1NDkxfQ.KS27hG-7fbhUjGsQSX5OX9fQ5w6NpVYpUgFDPsLrzN4", #akash 3
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZWYyOGU1YjE1ODYxYTkwYjFlNmFhNiIsIm1vYmlsZSI6Ijc5NzQ4ODkwNzMiLCJmaXJzdE5hbWUiOiI3OSoqKio5MDczIiwiaWF0IjoxNjE0NTY1NTkyfQ.O6YsArmCXbj_NJ9z4ApGhu3R8fJAYf8xbs4ecp6NgtQ" # akash 4
        
)

#===========================================================

#webhook = Webhook("https://discord.com/api/webhooks/792751034501038101/qzaAmoXwsetfIDDpdQe3TDDqRPzxBmUxC3uX_ycTcqpmmR0Y2P5tfNeccD9XeU2JCBxc")
webhook  = Webhook("https://discord.com/api/webhooks/768120385492221982/n6hDgLXGnojKQVpwH6hZy4jPqfRmTP-Rg1Yy3AWfixtZfEqLFbuy5R9lh7BH9zcro2G_")

class MainControllerAlreadyExistsError(Exception):
    pass

class Emulator:
    counts = 0
    mainController = None
    def __init__(self,authToken=None,isMain=False,isFriend=False):
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
        headers = {"user-agent": "okhttp/3.12.12","accept": "application/json, text/plain, */*","accept-encoding": "gzip"}
        response = requests.get(url,headers=headers,verify=self.verify).json()
        return response.get("upcomingEvents")

    def getLatestEvent(self):
        return self.getEvents()[0]

    def getEventDetails(self,eventId):
        url = f"https://api.fangame.live/event/getEventDetails?eventId={eventId}"
        headers = {"user-agent": "okhttp/3.12.12","accept": "application/json, text/plain, */*","accept-encoding": "gzip"}
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
        print(response)
        return response
    
    def user_authanticate(self,socketId,eventId,secretId=None):
        url = "https://api.fangame.live/pusher/user-authenticate"
        headers = {"x-auth-token": self.authToken,
        "content-type": "application/x-www-form-urlencoded",
        "content-length": "69",
        "accept-encoding": "gzip",
        
        "user-agent": "okhttp/3.12.12"}
        if not secretId:
            payload = f"socket_id={socketId}&channel_name=private-{eventId}"
        else:
            payload = f"socket_id={socketId}&channel_name=private-{eventId}-{secretId}"
        response = requests.post(url,headers=headers,data=payload,verify=self.verify).json()
        return response['auth']
        
    
    def joinEvent(self,eventId,socketId):
        url = "https://api.fangame.live/pusher/join-event"
        headers = {"accept": "application/json, text/plain, */*",
        "x-auth-token": self.authToken,
        "content-type": "application/json;charset=utf-8",
        "content-length": "65",
        "accept-encoding": "gzip",
        
        "user-agent": "okhttp/3.12.12"}
        payload = {"eventId": eventId,"socketId":socketId}
        response = requests.post(url,headers=headers,json=payload,verify=self.verify).json()
        secretEventId = response['agoraChannelToken']['id']
        self.agoraId = response['agoraChannelToken']['id']
        return secretEventId

    def getLeaks(self,eventId,countNumber=1):
        currentQuestionNumber = self.questions.get("questionNumber")
        event = self.getEventDetails(eventId)
        event = event['eventDetails']
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
        #webhook.send(embed=embed)
        return correctAnswerOption , lastQuestionDetails['qid'] , embed

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
        payload = {"answer":{"qid":qid,"option":correct,"seconds":seconds},"eventId":self.eventId,"user":{"id":self.agoraId,"mobile":self.number,"firstName":self.firstName}}
        response = requests.post(url,headers=headers,json=payload).json()
        msg= f"Emulator Id {self.Id}: Submitted Answer! || [{response}]"
        print(msg)

    def getLeaderboard(self,eventId):
        url = f"https://api.fangame.live/pusher/{eventId}/leader-board?"
        headers = {"accept":"application/json, text/plain, */*","user-agent":"okhttp/3.12.1","cookie": self.cookies,"x-auth-token":self.authToken}
        response =  requests.get(url,headers=headers,verify=self.verify).json()
        if response['msg'] == "Please try after sometime":
            time.sleep(20)
            return self.getLeaderboard(eventId)
        return response['leaderBoard']
        
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
                    #correct,qid = self.getLeaks(self.eventId)
                    self.submitAnswer(qid,correct)
                    for emu in emus:
                        threading.Thread(target = emu.submitAnswer, args = [qid, correct]).start()
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
        #if self.isMain is True:
        self.ws = websocket.WebSocketApp(url,on_message = on_message,on_error = on_error,on_close = on_close)
        #else:
        #    self.ws = websocket.WebSocketApp(url,on_error = on_error,on_close = on_close)
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
    while True:
        event = Emulator().getLatestEvent()
        eventId = event.get("_id")
        eventName = event['eventName']
        eventTime = event['eventTime']/1000
        currentTime = int(time.time())
        timeLeft = eventTime - currentTime -600
        if timeLeft>0:
            print(f"Sleeping for {timeLeft} secs")
            time.sleep(timeLeft)
        
        mainController = Emulator(mainControllerToken,isMain=True)
        
        mainController.setEventId(eventId)
        mainThread = threading.Thread(target=mainController.connect)
        mainThread.start()
        print(mainController)

    
