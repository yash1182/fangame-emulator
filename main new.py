import time
import requests
import json
from requests.api import head
import websocket
import threading
from dhooks import Embed, Webhook
from urllib.parse import quote
import gsearch
import pusherclient

embedColor = 0xFF6347
questions = {}

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZjA5Y2FiY2YzNTNjY2U0NGI3OGVkMCIsIm1vYmlsZSI6Ijg0MzUzNTkwNTYiLCJmaXJzdE5hbWUiOiJBc2hvayBHdXB0YSIsImlhdCI6MTYwOTYxNDc3OX0.NV2IFAfr3HmeIcLYoABT7siRC8_z1-SlVACOhIiEdww"

embedUrl = ""
webhook = Webhook("https://discord.com/api/webhooks/792751034501038101/qzaAmoXwsetfIDDpdQe3TDDqRPzxBmUxC3uX_ycTcqpmmR0Y2P5tfNeccD9XeU2JCBxc")

cookies = None
eventId = None

questions = {}

def getEvents():
    global eventId
    url = "https://api.fangame.live/event/getEvents?page=undefined"
    headers = {"accept":"application/json, text/plain, */*"}
    response = requests.get(url).json()
    events = response['upcomingEvents']
    event = events[0]    
    eventId = event['_id']
    return eventId
    
def getEventDetails(eventId):
    url = f"https://api.fangame.live/event/getEventDetails?eventId={eventId}"
    headers = {"accept":"application/json, text/plain, */*"}
    response =requests.get(url,headers=headers).json()
    return response
    
def getLeaks(eventId,countNumber=1):
    time.sleep(1)
    currentQuestionNumber = questions.get("questionNumber")
    response = getEventDetails(eventId)
    lastQuestionDetails = response['eventDetails']['lastQuestionDetails']
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

def submitAnswer(ws,qid,correctAnswer):
    payload = '42["submitAnswer",{"qid":"'+qid+'","option":'+correctAnswer+',"seconds":8}]'
    print(payload)
    ws.send(payload)
    print("successfully submited answer")
    

def on_message(ws,message):
    global questions
    print(message)
    message = json.loads(message)
    if message.get("event") == "pusher:connection_established":
        data = json.loads(message['data'])
        socketId = data['socket_id']
        eventId = getEvents()
        auth = authanticate(eventId,socketId)
        js = {"event":"pusher:subscribe","data":{"channel":f"private-{eventId}","auth":f"{auth}"}}
        ws.send(json.dumps(js,separators = (",", ":")))
        
def on_error(ws,error):
    print(error)
def on_close(ws):
    print("connection closed")

def pingTask(ws):
    while True:
        time.sleep(5)
        ws.send("2")
        
def authanticate(eventId=None,socketId=None):
    url = "https://api.fangame.live/pusher/user-authenticate"
    postheaders = {"x-auth-token": f"{token}",
        "content-type": "application/x-www-form-urlencoded",
        "accept-encoding": "gzip",
        "cookie": cookies,
        "user-agent": "okhttp/3.12.1"}
    if not socketId:

        payload = f"socket_id=6128.10180848&channel_name=private-{eventId}"
    else:
        payload = f"socket_id={socketId}&channel_name=private-{eventId}"
    response = requests.post(url,headers=postheaders,data=payload).json()
    print(response)
    auth = response['auth']
    return auth
import pysher
def connectWebsocket(eventId):
    global cookies
    def on_open(ws):
        print("Connected to FanGame Live")
        
    url = "wss://ws-ap2.pusher.com/app/96c057b918de826b8ea3?protocol=7&client=js&version=7.0.2&flash=false"
    ws = websocket.WebSocketApp(url,on_message = on_message,on_error = on_error,on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
    

if __name__ == "__main__":
    eventId = getEvents()
    #eventId = "5feb2c09da84617d030f8778"
    getEventDetails(eventId)
    connectWebsocket(eventId)
