import time
import requests
import json
from requests.api import head
import websocket
import threading
from dhooks import Embed, Webhook
from urllib.parse import quote
import gsearch
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
    print(response)
    events = response['upcomingEvents']
    event = events[0]    
    eventId = event['_id']
    print(eventId)
    #eventId = "5fe30e2759a0103ad1a1af5e"
    return eventId
    
def getEventDetails(eventId):
    url = f"https://api.fangame.live/event/getEventDetails?eventId={eventId}"
    headers = {"accept":"application/json, text/plain, */*"}
    response =requests.get(url,headers=headers,verify=False).json()
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
        googlelink = f"https://google.com/search?q="
        googleWOAnswers = googlelink+quote(question)
        #embed = Embed(title=f"{question}",color=embedColor)
        embed = Embed(title=f"{question}",url=googleWOAnswers,color=embedColor)
        webhook.send(embed=embed)
        questions['question'] = question
        questions['questionNumber'] = questionNumber
    if message[0]=="options":
        options = message[1]
        option1 = options[0]
        option2 = options[1]
        option3 = options[2]
        option4 = options[3]
        questions['options'] = options
        question = questions['question']
        embed = Embed(title=f"{question}",color=embedColor)
        optionNumber = 1
        for option in options:
            embed.add_field(name=f"Option {optionNumber}:",value=f"{option}",inline=False)
            optionNumber+=1
        webhook.send(embed=embed)
        response = gsearch.googlesearch(question,options).results()
        if response.get("scores"):
            score = response['scores']
            embed = Embed(title=f"Results:",description=f"**{options[0]}: {score[options[0]]}\n{options[1]}: {score[options[1]]}\n{options[2]}: {score[options[2]]}\n{options[3]}: {score[options[3]]}**",color=embedColor)
            embed.set_footer(text="Tamasha | The Unfortunate Guy#7835 |")
            webhook.send(embed=embed)
        #correct,qid = getLeaks(eventId)
        #submitAnswer(ws,qid,correct)
        #payload = '42["submitAnswer",{"qid":"'+qid+'","option":'+correct+',"seconds":5}]'
        #payload = "42"+ json.dumps(["submitAnswer",{"qid":qid,"option":int(correct),"seconds":5}],separators = (",", ":"))
        #print(payload)
        #ws.send(payload)
        #print("successfully submited answer")


    if message[0] == "correctAnswer":
        data = message[1]
        correctAnswerOption =data['answer']

    print(message)


def on_error(ws,error):
    print(error)
def on_close(ws):
    print("connection closed")

def pingTask(ws):
    while True:
        time.sleep(5)
        ws.send("2")
        

def on_open(ws):
    print("Connected to FanGame Live")
    ws.send("2probe")
    ws.send("5")
    t2=threading.Thread(target=pingTask,args=(ws,))
    t2.start()

def connectWebsocket(eventId):
    global cookies
    url = f"https://api.fangame.live/socket.io/?token={token}&EIO=3&transport=polling"
    response = requests.get(url)
    cookies = response.cookies
    ioCookie = dict(cookies)['io']
    response = json.loads(response.text[4:])
    sid = response['sid']
    pingInterval = response['pingInterval']
    pingTimeout = response['pingTimeout']
    #=========================================
    url = f"{url}&sid={sid}"
    headers = {"cookie":f"io={ioCookie}"}
    response=requests.get(url,headers=headers).text
    print(response)
    #=========================================
    payload = '42:42["joinEvent","'+eventId+'"]'
    response= requests.post(url,headers=headers,data=payload).text
    print(response)
    #=========================================
    response= requests.get(url,headers=headers).text
    print(response)
    #=========================================
    print("---------------------")
    url = f"wss://api.fangame.live/socket.io/?token={token}&EIO=3&transport=websocket&sid={sid}"
    ws = websocket.WebSocketApp(url,header=headers,on_message = on_message,on_error = on_error,on_close = on_close)
    ws.on_open = on_open
    ws.run_forever(ping_interval=pingInterval,ping_timeout=pingTimeout)

    

if __name__ == "__main__":
    eventId = getEvents()
    #eventId = "5feb2c09da84617d030f8778"
    getEventDetails(eventId)
    connectWebsocket(eventId)
