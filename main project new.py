import time
import requests
import json
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

#mainControllerToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZjA4MGM3Y2YzNTNjY2U0NGI3ODdhOCIsIm1vYmlsZSI6Ijk2Njk3MDkxNzkiLCJmaXJzdE5hbWUiOiI5NioqKio5MTc5IiwiaWF0IjoxNjA5NjA4ODQ5fQ.Gv9VE8WXlMjoZz0Mt-C-tMchegxALx4Gv1WQ5Cg5mnk" #mummy 
mainControllerToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYwMWUzZDg4NzE3NWEzYzM0YzIxZWM5OSIsIm1vYmlsZSI6IjkzMDEyNzEyMTAiLCJmaXJzdE5hbWUiOiJzdW1hbiIsInNvdXJjZSI6IlN5RlFOdklDRGMiLCJpYXQiOjE2MTMzNzA5NDJ9._IIruopgvuuDsAcNuMD8-r8pmF2NS4MI691xnt5BTu0" #9301271210
#mainControllerToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYwMWUzOWYxMTI0YmI3YTliOGYwMTNjMSIsIm1vYmlsZSI6Ijk4MjYxNDEyMDciLCJmaXJzdE5hbWUiOiI5OCoqKioxMjA3Iiwic291cmNlIjoiU3lGUU52SUNEYyIsImlhdCI6MTYxMzM3MTA2N30.EVMfDLOiIKOfFWOeIWeH_Ev9F4Yj2CUcKHEaMiqDu0M"
tokens =(
        )

users = {
    }

firstRankUsers = []


webhook = Webhook("https://discord.com/api/webhooks/792751034501038101/qzaAmoXwsetfIDDpdQe3TDDqRPzxBmUxC3uX_ycTcqpmmR0Y2P5tfNeccD9XeU2JCBxc")

def publish(message):
    return
    webhook.send(message)

class MainControllerAlreadyExistsError(Exception):
    pass

class FanGameUser:
    def __init__(self,authToken=None):
        self.authToken = authToken
        if self.authToken:
            userInfo = jwt.decode(self.authToken, options={"verify_signature": False},algorithms=["HS256"])
            self.number = userInfo['mobile']
            self.firstName = userInfo['firstName']
            self.userId = userInfo['id']
            self.prize = 0
            
    def __str__(self):
        js = {"number":self.number,"name":self.firstName,"userId":self.userId}
        return json.dumps(js)
    def setPrize(self,amount:int=0):
        self.prize = amount

class PrizeCalculator:
    def __init__(self,winnerDetails:list=[],date:datetime=datetime.datetime.now().date()):
        self.date = date
        self.winnerDetails = winnerDetails
        self.users = {}
        for user in users.items():
            self.users[user[0]] = [FanGameUser(authToken) for authToken in user[1]]
    def calculate(self):
        for user,accounts in self.users.items():
            for account in accounts:
                for winner in self.winnerDetails:
                    if winner['userId'] == account.userId:
                        prize = winner['totalAmount']
                        if not prize:
                            prize = 0
                        account.setPrize(prize)
                        break
    def display(self):
        print(f"Prize Distribution for {self.date}")
        for user,accounts in self.users.items():
            totalAmount = 0
            for account in accounts:
                totalAmount+=account.prize
            print(f"{user}: {totalAmount}")    

#===================================================================
class Emulator:
    counts = 0
    mainController = None
    def __init__(self,authToken=None,isMain=False,isFriend=False):
        if Emulator.mainController:
            if isMain:
                raise MainControllerAlreadyExistsError
        self.verify = False
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
    def setEventId(self,eventId)->None:
        self.eventId = eventId
        url = f"https://api.fangame.live/user/getAgoraTokenTEMP?eventId={eventId}"
        headers = {"accept":"application/json, text/plain, */*","user-agent":"okhttp/3.12.1","x-auth-token":self.authToken}
        response = requests.get(url,headers=headers,verify=self.verify).json()
        self.agoraId = response['id']
        print(f"agora ID: {self.agoraId}")

    def setAuthToken(self,authToken)->None:
        self.authToken = authToken
    def getEvents(self):
        url = "https://api.fangame.live/event/getEvents?page=undefined"
        headers = {"accept":"application/json, text/plain, */*","x-source-app":"SyFQNvICDc"}
        response = requests.get(url,headers=headers,verify=self.verify).json()
        events = response['upcomingEvents']
        event = events[0]   
        eventName = event['eventName']
        print(f"Starting Emulators for {eventName}")
        eventId = event['_id']
        return eventId
    def getEventsList(self):
        url = "https://api.fangame.live/event/getEvents?page=undefined"
        headers = {"accept":"application/json, text/plain, */*","x-source-app":"SyFQNvICDc"}
        response = requests.get(url,headers=headers,verify=False).json()
        return response
    def getEventDetails(self,eventId):
        url = f"https://api.fangame.live/event/getEventDetails?eventId={eventId}&userId={self.userId}"
        headers = {"accept":"application/json, text/plain, */*","x-source-app":"SyFQNvICDc"}
        response =requests.get(url,headers=headers,verify=self.verify).json()
        return response
    def registerForEvent(self):
        response = self.getEventDetails(self.eventId)
        if response['isRegistered'] is True:
            return
        url = "https://api.fangame.live/event/registerForEvent"
        headers = {"x-auth-token": f"{self.authToken}","content-type": "application/json","accept-encoding": "gzip","cookie": self.cookies,"user-agent": "okhttp/3.12.1"}
        payload = {"eventId": self.eventId}
        response =requests.post(url,headers=headers,json=payload,verify=self.verify).json()
        print(response)
    def getAuth(self,eventId,socketId,secretId=None) -> dict:
        url = "https://api.fangame.live/pusher/user-authenticate"
        headers = {"x-auth-token": f"{self.authToken}","content-type": "application/x-www-form-urlencoded","accept-encoding": "gzip","cookie": self.cookies,"user-agent": "okhttp/3.12.1"}
        if not secretId:
            payload = f"socket_id={socketId}&channel_name=private-{eventId}"
        else:
            payload = f"socket_id={socketId}&channel_name=private-{eventId}-{secretId}"
        response = requests.post(url,headers=headers,data=payload,verify=self.verify).json()
        auth = response['auth']
        return auth

    def getLeaks(self,eventId,countNumber=1):
        currentQuestionNumber = self.questions.get("questionNumber")
        response = self.getEventsList()
        events = response['upcomingEvents']
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
                #webhook.send(embed=embed)
                return correctAnswerOption , lastQuestionDetails['qid']

    def walletDetails(self):
        url = "https://api.fangame.live/user/wallet/walletDetails"
        headers = {"accept":"application/json, text/plain, */*","user-agent":"okhttp/3.12.1","x-auth-token":self.authToken}
        response = requests.get(url,headers=headers,verify=self.verify).json()
        details = response['walletDetails']
        withdrawableBalance = details['withdrawableBalance']
        totalBalance = details['totalBalance']
        allCreditBalance = details['allCreditBalance']
        return details

    def cashout(self):
        amount = self.walletDetails()['withdrawableBalance']
        if amount ==0:
            print("You have insufficent Balance.")
            return {"message":"You have insufficent Balance."}
        url = "https://api.fangame.live/user/wallet/withdrawal"
        headers = {"accept":"application/json, text/plain, */*","user-agent":"okhttp/3.12.1","x-auth-token":self.authToken}
        payload = {"withdrawalAmount":amount}
        response = requests.post(url,headers=headers,json=payload,verify=self.verify).json()
        print(response['msg'])
        return {"message":response['msg']}

    def transactionDetails(self):
        url = "https://api.fangame.live/user/transactionHistory?"
        headers = {"accept":"application/json, text/plain, */*","user-agent":"okhttp/3.12.1","x-auth-token":self.authToken}
        response = requests.get(url,headers=headers,verify=self.verify).json()
        transactions = response['transactions']
        for transaction in transactions:
            totalAmount = transaction['totalAmount']
            type = transaction['type']
            print(f"{type}: {totalAmount}")
            print("==================")

    def prizeCalculator(self,winnerDetails:list):
        for winner in winnerDetails:
            if winner['mobile'] == self.number:
                self.winnerDetails = winner
                break
        self.winPrize = self.winnerDetails['totalAmount']
        

    def submitAnswer(self,qid,correct):
        url = "https://api.fangame.live/pusher/submit-answer"
        headers = {"accept":"application/json, text/plain, */*","user-agent":"okhttp/3.12.12","cookie": self.cookies,"x-auth-token":self.authToken,"accept-encoding": "gzip"}
        second = 8
        #if self not in firstRankUsers:
        #    second = random.choice((8,9))
        payload = {
            "answer": {
                "qid": qid,
                "option": correct,
                "seconds": second
            },
            "eventId": self.eventId,
            "user": {
		"id": "601e3d887175a3c34c21ec99",
		"mobile": "9301271210",
		"firstName": "suman",
		"source": "SyFQNvICDc"
	    }
        }    
        print(payload)
        response = requests.post(url,headers=headers,json=payload).json()
        msg= f"Emulator Id {self.Id}: Submitted Answer! || [{response}]"
        print(msg)
        publish(msg)

    def joinEvent(self,eventId,socketId):
        url = "https://api.fangame.live/pusher/join-event"
        headers = {"accept":"application/json, text/plain, */*",
        "x-auth-token":self.authToken,
        "content-type":"application/json;charset=utf-8"}
        payload = {"eventId": eventId,"socketId": socketId}
        response =  requests.post(url,headers=headers,json=payload,verify=self.verify)
        response = response.json()
        secretEventId = response['agoraChannelToken']['id']
        #self.agoraId = secretEventId
        #print("agora id: "+self.agoraId)
        return secretEventId
    
    def getLeaderboard(self,eventId):
        url = f"https://api.fangame.live/pusher/{eventId}/leader-board?"
        headers = {"accept":"application/json, text/plain, */*","user-agent":"okhttp/3.12.1","cookie": self.cookies,"x-auth-token":self.authToken}
        response =  requests.get(url,headers=headers,verify=self.verify).json()
        if response['msg'] == "Please try after sometime":
            time.sleep(20)
            return self.getLeaderboard(eventId)
        return response['leaderBoard']

    def connect(self):
        self.registerForEvent()
        def on_open(ws):
            if self.isMain is True:
                msg = "Main Controller Connected!"
                print(msg)
                publish(msg)
            else:
                msg = f"Emulator Account Id {self.Id} Connected!"
                print(msg)
                publish(msg)
        def on_error(ws,error):
            msg = f"Emulator Id {self.Id} error: {str(error)}"
            print(msg)
            publish(msg)
        def on_close(ws):
            msg = f"Emulator Id {self.Id}: Connection Closed!"
            print(msg)
            publish(msg)
        def on_message(ws,message):
            print(message)
            message = json.loads(message)
            data = json.loads(message['data'])
            #================================================
            if message.get("event") == "pusher:connection_established":
                socketId = data['socket_id']
                eventId = self.eventId
                
                auth = self.getAuth(self.eventId,socketId)
                js = {"event":"pusher:subscribe","data":{"channel":f"private-{eventId}","auth":f"{auth}"}}
                self.ws.send(json.dumps(js,separators = (",", ":")))
                auth2 = self.user_authanticate(socketId,self.eventId,self.userId)
                js = {"event":"pusher:subscribe","data":{"auth":auth2,"channel":f"private-{self.eventId}-{self.userId}"}}
                self.ws.send(json.dumps(js,separators = (",", ":")))
                self.joinEvent(self.eventId,socketId)
            #================================================
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
                    correct,qid = self.getLeaks(self.eventId)
                    self.submitAnswer(qid,correct)
                    #for emu in emus:
                    #    threading.Thread(target = emu.submitAnswer, args = [qid, correct]).start()
                    #self.getLeaks(self.eventId)
                except Exception as e:
                    print(e)
            if message.get('event') == "totalScores":
                totalScores = self.getLeaderboard(self.eventId)
                with open(f"{cd}\{datetime.datetime.now().date()}.json","w+") as f:
                    json.dump(totalScores,f)
                print("successfully dumped today's winner details")
                ws.close()
                for emu in emus:
                    threading.Thread(target = emu.ws.close).start()


        url = "wss://ws-ap2.pusher.com/app/7c0e1751e3e734fc0273?protocol=7&client=js&version=7.0.2&flash=false"
        if self.isMain is True:
            self.ws = websocket.WebSocketApp(url,on_message = on_message,on_error = on_error,on_close = on_close)
        else:
            self.ws = websocket.WebSocketApp(url,on_error = on_error,on_close = on_close)
        self.ws.on_open = on_open
        self.ws.run_forever()

emus = [Emulator(token) for token in tokens]


def start(eventId=None):
    if not eventId:
        eventId = Emulator().getEvents()
    for emu in emus:
        emu.setEventId(eventId)
    threads = [threading.Thread(target=emu.connect) for emu in emus]
    for thread in threads:
        thread.start()

def getFirstRank():
    global firstRankUsers
    while len(firstRankUsers)!=3:
        firstRankUsers.append(random.choice(emus))

if __name__ == "__main__":
    #'''
    random.shuffle(emus)
    eventId = Emulator().getEvents()
    mainController = Emulator(mainControllerToken,isMain=True)
    mainController.setEventId(eventId)
    #mainController.cashout()
    mainThread = threading.Thread(target=mainController.connect)
    mainThread.start()
    print(mainController)
    '''
    getFirstRank()
    for emu in emus:
        print(emu)
        #emu.cashout()
    start(eventId)
    cd = os.path.dirname(os.path.realpath(__file__))
    date = datetime.datetime.now().date()
    date = "2021-01-23"
    with open(cd+rf"\{date}.json","r+",encoding="utf8") as f:
        winnerDetails = json.load(f)
    calculator = PrizeCalculator(winnerDetails)
    calculator.calculate()
    calculator.display()
    #'''


    
