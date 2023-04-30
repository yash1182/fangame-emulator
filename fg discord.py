import time
import requests
import json
from requests.api import head, options
from requests.models import Response
import websocket
import sys
import threading
import asyncio
import discord
from dhooks import Webhook, Embed
from discord.ext import commands
from discord.ext.commands import Bot, CommandNotFound
from dhooks import Embed, Webhook
import datetime
import jwt
import os
from bs4 import BeautifulSoup
import gsearch
import random
from urllib.parse import quote
import logging

cd = os.path.dirname(os.path.realpath(__file__))

embedColor = 0xFF6347

botprefix = "+"
bot = commands.Bot(command_prefix=botprefix)
bot.remove_command('help')


@bot.event
async def on_ready():
    print("Logged in as " + bot.user.name)
    print("I'm ready")

mainControllerToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYwMjhiYjEyZjhmNTM5NDUyMzE3ZTYxNiIsIm1vYmlsZSI6IjgwNzcyMTMyMDUiLCJmaXJzdE5hbWUiOiJBbml0YSIsInNvdXJjZSI6IlN5RlFOdklDRGMiLCJpYXQiOjE2MTM2NTgzMDl9.7uafdpmnNcEU16PeCYqrMCJVL3yN6XLpZtenxuERkX4"  # mummy

tokens = (
    # "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZjVjODc0ZTE1MjQxMWJkYzg3MTE1NyIsIm1vYmlsZSI6Ijg1MjA4MzM5MDkiLCJmaXJzdE5hbWUiOiI4NSoqKiozOTA5IiwiaWF0IjoxNjEzNjU4NDgzfQ.1JNONnI7915zvDO-E7LpXhC4Fix4g0gbgtIe5vNgPLg",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTg5OTg1ZjA2YTFmNTJkMDY3YTc1NSIsIm1vYmlsZSI6IjkzMDEyNzEyMTAiLCJmaXJzdE5hbWUiOiI5MyoqKioxMjEwIiwiaWF0IjoxNjA5NTk2ODU0fQ.gMr3kFsRwiRD_Mx88BYKT1YauUwhQkYUP4Q9Vc-651M",  # 9301271210
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTg4ZDEyZjA2YTFmNTJkMDY3OWUwYyIsIm1vYmlsZSI6Ijk4MjYxNDEyMDciLCJmaXJzdE5hbWUiOiJhbWl0IiwiaWF0IjoxNjA5OTE5MjY0fQ.ywUzJruJncXW47qs0xmg5AiZxk95ajqH3UaybbinHz0",  # main number
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZjA5Y2FiY2YzNTNjY2U0NGI3OGVkMCIsIm1vYmlsZSI6Ijg0MzUzNTkwNTYiLCJmaXJzdE5hbWUiOiJBc2hvayBHdXB0YSIsImlhdCI6MTYwOTYxNDc3OX0.NV2IFAfr3HmeIcLYoABT7siRC8_z1-SlVACOhIiEdww",  # ashok
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTVhNDU3MzQ4N2ExNzZlMmI3ZGI5ZSIsIm1vYmlsZSI6Ijk3NzM4MzM5NzIiLCJmaXJzdE5hbWUiOiJQcmluY2UiLCJpYXQiOjE2MDk4NTI4OTB9.k0hXVINO3TfCH3gXbGLF4Eei_kPgFfoTLsT_bE-IMAk",  # abhi-1
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTg5OTI1ZjA2YTFmNTJkMDY3YTcxZSIsIm1vYmlsZSI6IjgwNzcyMTMyMDUiLCJmaXJzdE5hbWUiOiJBYmhpIiwiaWF0IjoxNjA5ODUzMTM0fQ.pRTnxvqEjvhVElbY3HPdoFS3A1OrPUUwnTooOe8biYA",  # abhi 2
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZjFlMmIyY2YzNTNjY2U0NGI3OWRkYyIsIm1vYmlsZSI6Ijk3NTM3OTIzNDkiLCJmaXJzdE5hbWUiOiI5NyoqKioyMzQ5IiwiaWF0IjoxNjA5ODM2MTk0fQ.MopqRg1hd5jEnsbuOSaP_aEkwQzN5i4Rp_59R2ZeJRQ",  # akash 1
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZTg5MGE0ZjA2YTFmNTJkMDY3OWVhZCIsIm1vYmlsZSI6IjcwMjQ4ODU3OTIiLCJmaXJzdE5hbWUiOiJDYXNhbm92YSIsImlhdCI6MTYwOTg1OTI0NH0._vKI7rDHJCNIfmz9WVQ6g6jk7Sbg4wjLHXYBE7lme60",  # akash 2
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYwM2M1MDViZDhhMmQ2OTM0YjA4NDJjMSIsIm1vYmlsZSI6Ijk0MDY5MTQ3NjgiLCJmaXJzdE5hbWUiOiI5NCoqKio0NzY4IiwiaWF0IjoxNjE0NTY1NDkxfQ.KS27hG-7fbhUjGsQSX5OX9fQ5w6NpVYpUgFDPsLrzN4",  # akash 3
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVmZWYyOGU1YjE1ODYxYTkwYjFlNmFhNiIsIm1vYmlsZSI6Ijc5NzQ4ODkwNzMiLCJmaXJzdE5hbWUiOiI3OSoqKio5MDczIiwiaWF0IjoxNjE0NTY1NTkyfQ.O6YsArmCXbj_NJ9z4ApGhu3R8fJAYf8xbs4ecp6NgtQ"  # akash 4

)

# ===========================================================

#webhook = Webhook("https://discord.com/api/webhooks/792751034501038101/qzaAmoXwsetfIDDpdQe3TDDqRPzxBmUxC3uX_ycTcqpmmR0Y2P5tfNeccD9XeU2JCBxc")
webhook = Webhook(
    "https://discord.com/api/webhooks/817567625914875914/DGZ1vjmlgDvzCG8bftDxkrROrQ6JV7iFDI-c0j6Ew8EGVGoZBu5l88m2mKBuW_8EZqC-")


class MainControllerAlreadyExistsError(Exception):
    pass


def getDirect(question, options=None):
    query = question.replace(" ", "%20")
    googlelink = "https://www.google.com/search?q="
    url = f"{googlelink}{query}&num=50"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'}
    page = requests.get(url, headers=headers).text
    soup = BeautifulSoup(page, 'html.parser')
    directText = soup.find('div', {"data-tts": "answers"})
    if directText:
        print(directText.text)
        embed = Embed(title="Direct Result Found!",
                      description=f"**{directText.text}**", color=0x800080)
        embed.set_footer(text="The Unfortunate Guy#7835 | HQ Trivia |")
        webhook.send(embed=embed)
        return


class Emulator:
    counts = 0
    mainController = None

    def __init__(self, authToken=None, isMain=False, isFriend=False, canWrong=0):
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
        self.isConnected = False
        self.canWrongRemaining = canWrong
        self.totalCanWrong = canWrong
        self.currentQID = None
        if self.isMain is True:
            Emulator.mainController = self
        if self.authToken != None:
            Emulator.counts += 1
            self.Id = Emulator.counts
            userInfo = jwt.decode(self.authToken, options={
                                  "verify_signature": False}, algorithms=["HS256"])
            self.number = userInfo['mobile']
            self.firstName = userInfo['firstName']
            self.userId = userInfo['id']
        self.ws = None
        self.winPrize = 0
        self.winnerDetails = {}
        self.questions = {}

    def __str__(self):
        js = {f"emulatorId": self.Id, "number": self.number,
              "name": self.firstName, "userId": self.userId, "isMain": self.isMain}
        return json.dumps(js)

    def getEvents(self):
        url = "https://api.fangame.live/event/getEvents?page=undefined"
        headers = {"user-agent": "okhttp/3.12.12", "accept": "application/json, text/plain, */*",
                   "accept-encoding": "gzip", "x-source-app": "SyFQNvICDc"}
        response = requests.get(url, headers=headers,
                                verify=self.verify).json()
        return response.get("upcomingEvents")

    def getLatestEvent(self):
        return self.getEvents()[0]

    def getEventDetails(self, eventId):
        url = f"https://api.fangame.live/event/getEventDetails?eventId={eventId}"
        headers = {"user-agent": "okhttp/3.12.12", "accept": "application/json, text/plain, */*",
                   "accept-encoding": "gzip", "x-source-app": "SyFQNvICDc"}
        response = requests.get(url, headers=headers,
                                verify=self.verify).json()
        return response

    def getAgoraTempToken(self, eventId):
        url = f"https://api.fangame.live/user/getAgoraTokenTEMP?eventId={eventId}"
        headers = {"user-agent": "okhttp/3.12.12", "accept": "application/json, text/plain, */*",
                   "accept-encoding": "gzip", "x-auth-token": self.authToken}
        response = requests.get(url, headers=headers,
                                verify=self.verify).json()
        return response

    def getAgoraRTMToken(self, eventId):
        url = f"https://api.fangame.live/user/getAgoraRTMTokenTEMP?eventId={self.eventId}"
        headers = {"user-agent": "okhttp/3.12.12", "accept": "application/json, text/plain, */*",
                   "accept-encoding": "gzip", "x-auth-token": self.authToken}
        response = requests.get(url, headers=headers,
                                verify=self.verify).json()
        return response

    def setEventId(self, eventId) -> None:
        self.eventId = eventId

    def registerForEvent(self, eventId):
        url = "https://api.fangame.live/event/registerForEvent"
        payload = {"eventId": self.eventId}
        headers = {"user-agent": "okhttp/3.12.12", "accept": "application/json, text/plain, */*", "accept-encoding": "gzip",
                   "x-auth-token": self.authToken, "content-type": "application/json", "content-length": "38"}
        response = requests.post(url, headers=headers,
                                 json=payload, verify=self.verify).json()
        print(f"Emulator id {self.Id}: {response}")
        return response

    def user_authanticate(self, socketId, eventId, secretId=None):
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
        response = requests.post(url, headers=headers,
                                 data=payload, verify=self.verify).json()
        return response['auth']

    def joinEvent(self, eventId, socketId):
        url = "https://api.fangame.live/pusher/join-event"
        headers = {"accept": "application/json, text/plain, */*",
                   "x-auth-token": self.authToken,
                   "content-type": "application/json;charset=utf-8",
                   "accept-encoding": "gzip",
                   "user-agent": "okhttp/3.12.12"}
        payload = {"eventId": eventId, "socketId": socketId}
        response = requests.post(url, headers=headers,
                                 json=payload, verify=self.verify).json()
        secretEventId = response['agoraChannelToken']['id']
        self.agoraId = response['agoraChannelToken']['id']
        return secretEventId

    def getLeaks(self, eventId, countNumber=1):
        currentQuestionNumber = self.questions.get("questionNumber")
        events = self.getEvents()
        for event in events:
            if event['_id'] == self.eventId:
                lastQuestionDetails = event['lastQuestionDetails']
                questionNumber = lastQuestionDetails['number']
                if questionNumber == 0:
                    return
                if currentQuestionNumber != questionNumber and questionNumber != 0:
                    if countNumber > 5:
                        return
                    time.sleep(1)
                    self.getLeaks(eventId, countNumber+1)
                    return
                question = lastQuestionDetails['question']
                options = lastQuestionDetails['options']
                correctAnswerOption = lastQuestionDetails['answer']
                embed = Embed(title=f"{question}")
                correctAnswer = options[correctAnswerOption-1]
                print(
                    f"Correct Answer:\n{correctAnswerOption}) {correctAnswer}")
                embed.add_field(name="Correct Answer:",
                                value=f"{correctAnswerOption}) {correctAnswer}")

                return correctAnswerOption, lastQuestionDetails['qid'], embed

    def submitAnswer(self, qid=None, correct=None):
        # if self.submitedAnswers > 1:
        seconds = 9
        # else:
        #    seconds = 8
        #    self.submitedAnswers += 2
        if not qid:
            qid = self.currentQID
        if not correct:
            return
        url = "https://api.fangame.live/pusher/submit-answer"
        headers = {"content-type": "application/json",
                   "content-length": "193",
                   "accept-encoding": "gzip",
                   "x-auth-token": self.authToken,
                   "user-agent": "okhttp/3.12.12"}
        payload = {"answer": {"qid": qid, "option": correct, "seconds": seconds}, "eventId": self.eventId, "user": {
            "id": self.userId, "mobile": self.number, "firstName": self.firstName, "source": "SyFQNvICDc"}}
        response = requests.post(url, headers=headers, json=payload).json()
        msg = f"Emulator Id {self.Id}: Submitted Answer! || [{response}]"
        print(msg)

    def submitAnswerFake(self, qid, correct):
        if self.submitedAnswers > 1:
            seconds = 9
        else:
            seconds = 8
            self.submitedAnswers += 2
        if self.canWrongRemaining > 0 and self.totalCanWrong <= 10:
            seconds = seconds - 1
            self.canWrongRemaining = self.canWrongRemaining - 1
        elif self.canWrongRemaining > 0:
            seconds = seconds - 1 - 1*(self.totalCanWrong//10)
            self.canWrongRemaining = self.canWrongRemaining - 1
        url = "https://api.fangame.live/pusher/submit-answer"
        headers = {"content-type": "application/json",
                   "content-length": "193",
                   "accept-encoding": "gzip",
                   "x-auth-token": self.authToken,
                   "user-agent": "okhttp/3.12.12"}
        payload = {"answer": {"qid": qid, "option": correct, "seconds": seconds}, "eventId": self.eventId, "user": {
            "id": self.userId, "mobile": self.number, "firstName": self.firstName, "source": "SyFQNvICDc"}}
        response = requests.post(url, headers=headers, json=payload).json()
        msg = f"Emulator Id {self.Id}: Submitted Answer! || [{response}]"
        print(msg)

    def getLeaderboard(self, eventId):
        url = f"https://api.fangame.live/pusher/{eventId}/leader-board?"
        headers = {"accept": "application/json, text/plain, */*",
                   "user-agent": "okhttp/3.12.12", "cookie": self.cookies, "x-auth-token": self.authToken}
        response = requests.get(url, headers=headers,
                                verify=self.verify).json()
        if response['msg'] == "Please try after sometime":
            time.sleep(20)
            return self.getLeaderboard(eventId)
        return response['leaderBoard']

    def getTransactionHistory(self, eventId=None):
        url = f"https://api.fangame.live/user/transactionHistory?"
        headers = {"accept": "application/json, text/plain, */*",
                   "user-agent": "okhttp/3.12.12", "x-auth-token": self.authToken}
        response = requests.get(url, headers=headers).json()
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
            self.isConnected = True
            if self.isMain is True:
                msg = "Main Controller Connected!"
                print(msg)
            else:
                msg = f"Emulator Account Id {self.Id} Connected!"
                print(msg)

        def on_error(ws, error):
            msg = f"Emulator Id {self.Id} error: {str(error)}"
            print(msg)

        def on_close(ws):
            msg = f"Emulator Id {self.Id}: Connection Closed!"
            print(msg)
            self.isConnected = False
        # =================================

        def on_message(ws, message):
            print(message)
            message = json.loads(message)
            data = json.loads(message['data'])
            eventType = message['event']
            if eventType == "pusher:connection_established":
                socketId = data['socket_id']
                auth1 = self.user_authanticate(socketId, self.eventId)
                js = {"event": "pusher:subscribe", "data": {
                    "auth": auth1, "channel": f"private-{self.eventId}"}}
                self.ws.send(json.dumps(js, separators=(",", ":")))

                auth2 = self.user_authanticate(
                    socketId, self.eventId, self.userId)
                js = {"event": "pusher:subscribe", "data": {"auth": auth2,
                                                            "channel": f"private-{self.eventId}-{self.userId}"}}
                self.ws.send(json.dumps(js, separators=(",", ":")))
                self.joinEvent(self.eventId, socketId)
                # =================================================
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
                embed = Embed(title=f"{question}",
                              url=googleWOAnswers, color=embedColor)
                webhook.send(embed=embed)
                self.questions['questionNumber'] = questionNumber
                self.currentQID = qid
            if message.get("event") == "options":
                options = data
                self.questions['options'] = options
                question = self.questions['question']
                qid = self.questions['qid']
                option1 = options[0]
                option2 = options[1]
                option3 = options[2]
                option4 = options[3]
                googlelink = f"https://google.com/search?q="
                allOptions = f'+("{option1}" OR "{option2}" OR "{option3}" OR "{option4}")'
                googleWOAnswers = googlelink+quote(f'{question}')
                googleWAnswers = googleWOAnswers+quote(f'{allOptions}')
                option1Link = googleWOAnswers+quote(f'{option1}')
                option2Link = googleWOAnswers+quote(f'{option2}')
                option3Link = googleWOAnswers+quote(f'{option3}')
                option4Link = googleWOAnswers+quote(f'{option4}')
                embed = Embed(title=f"{question}", url=googleWOAnswers,
                              description=f"[{option1}]({option1Link})\n\n[{option2}]({option2Link})\n\n[{option3}]({option3Link})\n\n[{option4}]({option4Link})\n\n", color=0x5761ee)
                embed.add_field(
                    name="Google:", value=f"[Google]({googleWOAnswers})\n\n[Google W/Options]({googleWAnswers})")

                webhook.send(embed=embed)
                response = gsearch.googlesearch(question, options).results()
                if response.get("scores"):
                    score = response['scores']
                    embed = Embed(
                        title=f"Results:", description=f"**{options[0]}: {score[options[0]]}\n{options[1]}: {score[options[1]]}\n{options[2]}: {score[options[2]]}\n{options[3]}: {score[options[3]]}**", color=0xff0000)
                    embed.set_footer(
                        text="The Unfortunate Guy#7835 | HQ Trivia |")
                    webhook.send(embed=embed)
                getDirect(question)

            if message.get("event") == "totalScores":
                webhook.send("Game Ended!")
                self.isConnected = False
                self.ws.close()

        # =================================
        url = "wss://ws-ap2.pusher.com/app/7c0e1751e3e734fc0273?protocol=7&client=js&version=7.0.2&flash=false"
        self.ws = websocket.WebSocketApp(
            url, on_message=on_message, on_error=on_error, on_close=on_close)
        self.ws.on_open = on_open
        self.ws.run_forever()


mainController = Emulator(mainControllerToken, isMain=True)


@bot.command()
async def events(ctx):
    events = Emulator().getEvents()
    embed = discord.Embed(title="FanGame Upcoming Events")
    counts = 0
    for event in events:
        eventId = event.get("_id")
        eventName = event['eventName']
        eventTime = event['eventTime']/1000
        currentTime = int(time.time())
        timeLeft = eventTime - currentTime - 600
        embed.add_field(name=f"{eventName}", value=f"{counts}", inline=False)
        counts += 1
    await ctx.send(embed=embed)


@bot.command()
async def connect(ctx, eventNumber=None):
    if mainController.isConnected is True:
        await ctx.send("Bot is already connected to a game!")
        return
    if not eventNumber:
        event = Emulator().getLatestEvent()
    else:
        event = Emulator().getEvents()[int(eventNumber)]
    eventId = event.get("_id")
    eventName = event['eventName']
    eventTime = event['eventTime']/1000
    currentTime = int(time.time())
    timeLeft = eventTime - currentTime - 600
    if timeLeft > 0:
        await ctx.send(f"**{eventName}, Sleeping for {timeLeft} secs.**")
        await asyncio.sleep(timeLeft)
    mainController.setEventId(eventId)
    mainThread = threading.Thread(target=mainController.connect)
    mainThread.start()
    await ctx.send(f"Bot connected to {eventName} successfully!")
    webhook.send(f"Bot connected to {eventName}")


@bot.command()
async def disconnect(ctx):
    if mainController.isConnected is False:
        await ctx.send("Bot is not connected to any game!")
        return
    mainController.ws.close()
    await ctx.send("Successfully Disconnected bot from the game!")


@bot.command()
async def restart(ctx):
    try:
        await ctx.send("Restarting bot!")
        os.startfile(__file__)
        sys.exit()
    except Exception as e:
        print(f"{str(e)}")


@bot.command()
async def send(ctx, answer=None):
    if not answer:
        return
    try:
        answer = int(answer)
        if answer not in (1, 2, 3, 4):
            raise Exception
        mainController.submitAnswer(correct=answer)
        await ctx.send("Answer Submitted!")
    except:
        await ctx.send("invalid input")

bot.run("")
