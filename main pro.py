import time
import requests
import json
from requests.api import head
import websocket
import threading
from dhooks import Embed, Webhook
from urllib.parse import quote
import pusherclient
import jwt

embedColor = 0xFF6347
questions = {}

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYwMWUzZDg4NzE3NWEzYzM0YzIxZWM5OSIsIm1vYmlsZSI6IjkzMDEyNzEyMTAiLCJmaXJzdE5hbWUiOiI5MyoqKioxMjEwIiwic291cmNlIjoiU3lGUU52SUNEYyIsImlhdCI6MTYxMjU5NDU4N30.MUPWC1mIl6tmodS1Yk4DPpBkNI1WpwXVMoszFw7HuAw"
userInfo = jwt.decode(token, options={"verify_signature": False},algorithms=["HS256"])
number = userInfo['mobile']
firstName = userInfo['firstName']
userId = userInfo['id']
embedUrl = ""
webhook = Webhook("https://discord.com/api/webhooks/792751034501038101/qzaAmoXwsetfIDDpdQe3TDDqRPzxBmUxC3uX_ycTcqpmmR0Y2P5tfNeccD9XeU2JCBxc")

cookies = None
eventId = None

questions = {}

def getEvents():
    global eventId
    url = "https://api.fangame.live/event/getEvents?page=undefined"
    headers = {"accept":"application/json, text/plain, */*","x-source-app":"SyFQNvICDc"}
    response = requests.get(url,headers=headers,verify=False).json()
    return response
    
def getEventDetails(eventId):
    url = f"https://api.fangame.live/event/getEventDetails?eventId={eventId}&userId={userId}"
    headers = {"accept":"application/json, text/plain, */*","x-source-app":"SyFQNvICDc"}
    response =requests.get(url,headers=headers).json()
    return response
def getLeaks(eventid,countNumber=1):
    global eventId
    currentQuestionNumber = questions.get("questionNumber")
    response = getEvents()
    events = response['upcomingEvents']
    for event in events:
        print(event['_id'])
        if event['_id'] == eventId:
            lastQuestionDetails = event['lastQuestionDetails']
            questionNumber = lastQuestionDetails['number']
            if questionNumber==0:
                return
            if currentQuestionNumber!= questionNumber and questionNumber!=0:
                if countNumber>5:
                    return
                time.sleep(1)
                getLeaks(eventId,countNumber+1)
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

def submitAnswer(qid,correctAnswer):
    payload = '42["submitAnswer",{"qid":"'+qid+'","option":'+correctAnswer+',"seconds":8}]'
    print(payload)
    print("successfully submited answer")
    
questions = {}
def on_message(ws,message):
    global questions
    print(message)
    message = json.loads(message)
    if message.get("event") == "pusher:connection_established":
        try:
            data = json.loads(message['data'])
            socketId = data['socket_id']
            print(socketId)
            response = getEvents()
            events = response['upcomingEvents']
            event = events[0]    #event number
            eventType =event['eventType']
            print(f"Event Type: {eventType}")
            eventId = event['_id']
            auth = authanticate(eventId,socketId)
            secretId =joinEvent(eventId,socketId)
            
            js = {"event":"pusher:subscribe","data":{"channel":f"private-{eventId}","auth":f"{auth}"}}
            ws.send(json.dumps(js,separators = (",", ":")))
            auth = authanticate(eventId,socketId,secretId)
            js = {"event":"pusher:subscribe","data":{"channel":f"private-{eventId}-{secretId}","auth":f"{auth}"}}
            ws.send(json.dumps(js,separators = (",", ":")))
        except Exception as e:
            print(e)
    data = json.loads(message['data'])
    if message.get("event") == "newQuestion":
        qid = data["qid"]
        questionNumber = data['number']
        question = data['question']
        questions['question'] = question
        questions['qid'] = qid
        googlelink = f"https://google.com/search?q="
        googleWOAnswers = googlelink+quote(question)
        embed = Embed(title=f"{question}",url=googleWOAnswers,color=embedColor)
        webhook.send(embed=embed)
        questions['questionNumber'] = questionNumber
        getLeaks("60267cb3e77a9a25023fefd4")
    if message.get("event") == "options":
        options = data
        questions['options'] = options
        question = questions['question']
        qid = questions['qid']
        embed = Embed(title=f"{question}",color=embedColor)
        optionNumber = 1
        for option in options:
            embed.add_field(name=f"Option {optionNumber}:",value=f"{option}",inline=False)
            optionNumber+=1
        webhook.send(embed=embed)
        
        
def on_error(ws,error):
    print(error)
def on_close(ws):
    print("connection closed")

def pingTask(ws):
    while True:
        time.sleep(5)
        ws.send("2")
        
def authanticate(eventId=None,socketId=None,secretId=None):
    url = "https://api.fangame.live/pusher/user-authenticate"
    postheaders = {"x-auth-token": f"{token}",
        "content-type": "application/x-www-form-urlencoded",
        "accept-encoding": "gzip",
        "cookie": cookies,
        "user-agent": "okhttp/3.12.1"}
    if not secretId:
        payload = f"socket_id={socketId}&channel_name=private-{eventId}"
    else:
        payload = f"socket_id={socketId}&channel_name=private-{eventId}-{secretId}"
    response = requests.post(url,headers=postheaders,data=payload).json()
    
    auth = response['auth']
    return auth

def joinEvent(eventId,socketId):
    url = "https://api.fangame.live/pusher/join-event"
    headers = {"accept":"application/json, text/plain, */*",
        "x-auth-token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYwMWUzZDg4NzE3NWEzYzM0YzIxZWM5OSIsIm1vYmlsZSI6IjkzMDEyNzEyMTAiLCJmaXJzdE5hbWUiOiI5MyoqKioxMjEwIiwic291cmNlIjoiU3lGUU52SUNEYyIsImlhdCI6MTYxMjU5NDU4N30.MUPWC1mIl6tmodS1Yk4DPpBkNI1WpwXVMoszFw7HuAw",
        "content-type":"application/json;charset=utf-8"}
    payload = {"eventId": eventId,"socketId": socketId}
    response =  requests.post(url,headers=headers,json=payload)
    print(response.text)
    response = response.json()
    secretEventId = response['agoraChannelToken']['id']
    return secretEventId


def connectWebsocket(eventId):
    global cookies
    def on_open(ws):
        print("Connected to FanGame Live")
        
    url = "wss://ws-ap2.pusher.com/app/7c0e1751e3e734fc0273?protocol=7&client=js&version=7.0.2&flash=false"
    ws = websocket.WebSocketApp(url,on_message = on_message,on_error = on_error,on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
    

if __name__ == "__main__":
    while True:
        response = getEvents()
        events = response['upcomingEvents']
        for event in events:
            eventType =event['eventType']
            eventId = event['_id']
            startTimeStamp = int(event['eventTime']/1000)
            currentTime = int(time.time())
            if ( startTimeStamp - 600 ) - currentTime < 0:
                #getEventDetails(eventId)
                connectWebsocket(eventId)
            else:
                print(f"sleeping for {( startTimeStamp - 600 ) - currentTime} seconds")
                time.sleep(( startTimeStamp - 600 ) - currentTime)


    
    
    eventId = "601e16a0124bb7a9b8f00e34"
    getEventDetails(eventId)
    connectWebsocket(eventId)
