import time
import requests
import json
import websocket
import threading
from dhooks import Embed, Webhook
import gsearch
from urllib.parse import quote
questions = {}
embedColor = 0xFF6347
embedUrl = "https://play-lh.googleusercontent.com/qTO_bSnkqmPFZ8k-vTFahIFDPl_iTyos_CMHVCRLq3RD78c30rQKT7S9yEdepLrRBw"
webhook = Webhook("https://discord.com/api/webhooks/792751034501038101/qzaAmoXwsetfIDDpdQe3TDDqRPzxBmUxC3uX_ycTcqpmmR0Y2P5tfNeccD9XeU2JCBxc")


   

def getEventDetails(eventId):
    url = f"https://api.fangame.live/event/getEventDetails?eventId={eventId}"
    headers = {"accept":"application/json, text/plain, */*"}
    response =requests.get(url,headers=headers).json()
    return response
    
def getLeaks(eventId,countNumber=1):
    time.sleep(1)
    currentQuestionNumber = questions.get("questionNumber")
    response = getEventDetails(eventId)
    print(response)
    lastQuestionDetails = response['eventDetails']['lastQuestionDetails']
    questionNumber = lastQuestionDetails['number']
    '''if questionNumber==0:
        return
    if currentQuestionNumber!= questionNumber and questionNumber!=0:
        if countNumber>5:
            return
        time.sleep(1)
        getLeaks(eventId,countNumber+1)
        return'''
    question = lastQuestionDetails['question']
    options = lastQuestionDetails['options']
    correctAnswerOption = lastQuestionDetails['answer']
    embed = Embed(title=f"{question}")
    correctAnswer = options[correctAnswerOption-1]
    print(f"{correctAnswerOption}) {correctAnswer}")
    embed.add_field(name="Correct Answer:",value=f"{correctAnswerOption}) {correctAnswer}")
    webhook.send(embed=embed)
    

def on_message(message):
    global questions
    if message=="3":
        return
    message = message[2:]
    message = json.loads(message)
    if message[0] == "agoraChannelToken":
        return
    if message[0] == "newQuestion":
        data = message[1]
        qid = data["qid"]
        questionNumber = data['number']
        questionNumber=11
        question = data['question']
        embed = Embed(title=f"{question}",color=embedColor)
        #webhook.send(embed=embed)
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
        #webhook.send(embed=embed)
        getLeaks("5fe2048159a0103ad1a1a835")

    if message[0] == "correctAnswer":
        data = message[1]
        correctAnswerOption =data['answer']
    if message[0]=="totalScores":
        data = message[1]
        
def submitAnswer(ws,qid,correctAnswer):
    payload = '42["submitAnswer",{"qid":"'+qid+'","option":'+correctAnswer+',"seconds":7}]'
    payload = "42"+ json.dumps(["submitAnswer",{"qid":qid,"option":int(correctAnswer),"seconds":3}],separators = (",", ":"))
    print(payload)
    #ws.send(payload)
    print("successfully submited answer")

if __name__ == "__main__":
    response = getEventDetails("600abbbc830ad382fb917362")
    lastQuestionDetails = response['eventDetails']['lastQuestionDetails']
    questionNumber = lastQuestionDetails['number']
    options = lastQuestionDetails['options']
    correctAnswerOption = lastQuestionDetails.get('answer')
    question = lastQuestionDetails.get('question')
    print(lastQuestionDetails)
    print("============================")
    print(f"Q. {question}")
    print(f"Correct Answer: {options[correctAnswerOption-1]}")
    #getLeaks("5feb2c09da84617d030f8778")
    #submitAnswer("hey","5feb2c09da84617d030f8778","3")
    #message = '42["newQuestion",{"qid":"5fe09bff8fb41099aceca623","number":10,"question":"The Obama campaign paid for in-game advertising in which game?"}]'
    #on_message(message)
    #message = '42["options",["Burnout Paradise","Fortnight","Minecraft","Call of Duty"]]'
    #on_message(message)