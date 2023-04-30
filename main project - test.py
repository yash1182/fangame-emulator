import time
import requests
import json
from requests.api import head
from requests.models import get_auth_from_url
import websocket
import threading
from dhooks import Embed, Webhook
from urllib.parse import quote
import jwt
embedColor = 0xFF6347

mainControllerToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZjA4MGM3Y2YzNTNjY2U0NGI3ODdhOCIsIm1vYmlsZSI6Ijk2Njk3MDkxNzkiLCJmaXJzdE5hbWUiOiI5NioqKio5MTc5IiwiaWF0IjoxNjA5NjA4ODQ5fQ.Gv9VE8WXlMjoZz0Mt-C-tMchegxALx4Gv1WQ5Cg5mnk"

tokens =(
        #"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTg5OTg1ZjA2YTFmNTJkMDY3YTc1NSIsIm1vYmlsZSI6IjkzMDEyNzEyMTAiLCJmaXJzdE5hbWUiOiI5MyoqKioxMjEwIiwiaWF0IjoxNjA5NTk2ODU0fQ.gMr3kFsRwiRD_Mx88BYKT1YauUwhQkYUP4Q9Vc-651M", #9301271210
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZjA5Y2FiY2YzNTNjY2U0NGI3OGVkMCIsIm1vYmlsZSI6Ijg0MzUzNTkwNTYiLCJmaXJzdE5hbWUiOiJBc2hvayBHdXB0YSIsImlhdCI6MTYwOTYxNDc3OX0.NV2IFAfr3HmeIcLYoABT7siRC8_z1-SlVACOhIiEdww",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTlkNTA0ZjA2YTFmNTJkMDY3YmNmZiIsIm1vYmlsZSI6Ijg4MjE4ODg4MTEiLCJmaXJzdE5hbWUiOiJhbnNodWwgc2hhcm1hIiwiaWF0IjoxNjA5NjE1MzAzfQ.IeMBeBrng6UQHqDaITeXJ5waYaek28L47yUNF-jnYL0",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZWFkNWFiZjA2YTFmNTJkMDY3Y2RlZCIsIm1vYmlsZSI6Ijk3MTE5ODY0ODciLCJmaXJzdE5hbWUiOiI5NyoqKio2NDg3IiwiaWF0IjoxNjA5Njc1MTQ1fQ.EczFpPU_nm-nIUXgbGmp_wn8Nnq5OJdem8TYtwYCD1o"
        )

webhook = Webhook("https://discord.com/api/webhooks/792751034501038101/qzaAmoXwsetfIDDpdQe3TDDqRPzxBmUxC3uX_ycTcqpmmR0Y2P5tfNeccD9XeU2JCBxc")

def publish(message):
    webhook.send(message)

class MainControllerAlreadyExistsError(Exception):
    pass

class Emulator:
    counts = 0
    mainController = None
    def __init__(self,authToken=None,isMain=False):
        if Emulator.mainController:
            if isMain:
                raise MainControllerAlreadyExistsError
        self.authToken = authToken
        self.eventId = None
        self.sessionId = None
        self.cookies = None
        self.pingInterval = 0
        self.pingTimeout = 0
        self.isMain = isMain
        if self.isMain is True:
            Emulator.mainController = self
        if self.authToken != None:
            Emulator.counts+=1
            self.Id = Emulator.counts
            userInfo = jwt.decode(self.authToken, options={"verify_signature": False},algorithms=["HS256"])
            self.number = userInfo['mobile']
            self.firstName = userInfo['firstName']
        self.ws = None
        self.questions = {}
    def __str__(self):
        js = {f"emulatorId":self.Id,"number":self.number,"name":self.firstName,"isMain":self.isMain}
        return json.dumps(js)
    def setEventId(self,eventId)->None:
        self.eventId = eventId
    def setAuthToken(self,authToken)->None:
        self.authToken = authToken
    def getEvents(self):
        url = "https://api.fangame.live/event/getEvents?page=undefined"
        headers = {"accept":"application/json, text/plain, */*"}
        response = requests.get(url).json()
        events = response['upcomingEvents']
        event = events[0]   
        eventId = event['_id']
        return eventId
    def getEventDetails(self,eventId):
        url = f"https://api.fangame.live/event/getEventDetails?eventId={eventId}"
        headers = {"accept":"application/json, text/plain, */*"}
        response =requests.get(url,headers=headers,verify=False).json()
        return response
    def getSession(self):
        url = f"https://api.fangame.live/socket.io/?token={self.authToken}&EIO=3&transport=polling"
        response = requests.get(url)
        cookies = response.cookies
        self.cookies = dict(cookies)['io']
        response = json.loads(response.text[4:])
        self.sessionId = response['sid']
        self.pingInterval = response['pingInterval']
        self.pingTimeout = response['pingTimeout']
        url = f"{url}&sid={self.sessionId}"
        headers = {"cookie":f"io={self.cookies}"}
        response=requests.get(url,headers=headers).text
        print(response)
        payload = '42:42["joinEvent","'+self.eventId+'"]'
        response= requests.post(url,headers=headers,data=payload).text
        print(response)
        response= requests.get(url,headers=headers).text
        print(response)

    def getLeaks(self,eventId,countNumber=1):
        time.sleep(1)
        currentQuestionNumber = self.questions.get("questionNumber")
        response = self.getEventDetails(eventId)
        lastQuestionDetails = response['eventDetails']['lastQuestionDetails']
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
        webhook.send(embed=embed)
        return correctAnswerOption , lastQuestionDetails['qid']

    def submitAnswer(self,qid,correct):
        payload = "42"+ json.dumps(["submitAnswer",{"qid":qid,"option":int(correct),"seconds":8}],separators = (",", ":"))
        self.ws.send(payload)
        msg= f"Emulator Id {self.Id}: Submitted Answer!"
        print(msg)
        publish(msg)
    def connect(self):
        if not self.sessionId:
            print("Session missing!")
            return
        #====================================================#
        def pingTask(ws):
            while True:
                time.sleep(5)
                ws.send("2")
        def on_open(ws):
            if self.isMain is True:
                msg = "Main Controller Connected!"
                print(msg)
                publish(msg)
            else:
                msg = f"Emulator Account Id {self.Id} Connected!"
                print(msg)
                publish(msg)
            ws.send("2probe")
            ws.send("5")
            t2=threading.Thread(target=pingTask,args=(ws,))
        def on_error(ws,error):
            msg = f"Emulator Id {self.Id}: {str(error)}"
            print(msg)
            publish(msg)
        def on_close(ws):
            msg = f"Emulator Id {self.Id}: Connection Closed!"
            print(msg)
            publish(msg)
        def on_message(ws,message):
            if message=="3":
                return
            print(message)
            message = message[2:]
            message = json.loads(message)
            if message[0] == "agoraChannelToken":
                return
            if message[0] == "newQuestion":
                data = message[1]
                qid = data["qid"]
                questionNumber = data['number']
                question = data['question']
                embed = Embed(title=f"{question}",color=embedColor)
                webhook.send(embed=embed)
                self.questions['question'] = question
                self.questions['questionNumber'] = questionNumber
            if message[0]=="options":
                options = message[1]
                self.questions['options'] = options
                question = self.questions['question']
                embed = Embed(title=f"{question}",color=embedColor)
                optionNumber = 1
                for option in options:
                    embed.add_field(name=f"Option {optionNumber}:",value=f"{option}",inline=False)
                    optionNumber+=1
                webhook.send(embed=embed)
                correct,qid = self.getLeaks(eventId)
                self.submitAnswer(qid,correct)
                for emu in emus:
                    print(emu)
                    emu.submitAnswer(qid,correct)
        #====================================================#
        url = f"wss://api.fangame.live/socket.io/?token={self.authToken}&EIO=3&transport=websocket&sid={self.sessionId}"
        headers = {"cookie":f"io={self.cookies}"}
        if self.isMain is True:
            self.ws = websocket.WebSocketApp(url,header=headers,on_message = on_message,on_error = on_error,on_close = on_close)
        else:
            self.ws = websocket.WebSocketApp(url,header=headers,on_error = on_error,on_close = on_close)
        self.ws.on_open = on_open
        self.ws.run_forever(ping_interval=self.pingInterval,ping_timeout=self.pingTimeout)


emus = [Emulator(token) for token in tokens]

def start(eventId=None):
    if not eventId:
        eventId = Emulator().getEvents()
    for emu in emus:
        emu.setEventId(eventId)
    for emu in emus:
        emu.getSession()
    threads = [threading.Thread(target=emu.connect) for emu in emus]
    for thread in threads:
        thread.start()

if __name__ == "__main__":
    eventId = Emulator().getEvents()
    mainController = Emulator(mainControllerToken,isMain=True)
    mainController.setEventId(eventId)
    mainController.getSession()
    mainThread = threading.Thread(target=mainController.connect)
    mainThread.start()
    print(mainController)
    for emu in emus:
        print(emu)
    start(eventId)


    
