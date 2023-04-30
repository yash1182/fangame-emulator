import asyncio
import websockets
import json
import requests
import os
cd = os.path.dirname(os.path.realpath(__file__))


connectedUsers = []
authSuccess = []
ActiveTokens = {}
masterSocket = None

MasterKey = "IAMTHEONE"

def users_event():
    return json.dumps({"type": "users", "count": len(connectedUsers)})

async def notify_users(websocket):
    for user in connectedUsers:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await user.send(message)
        

async def unregister(websocket):
    global connectedUsers
    global ActiveTokens
    global authSuccess
    global masterSocket
    if websocket in authSuccess and websocket in ActiveTokens.values():
        for tokens in ActiveTokens.copy():
            if ActiveTokens[tokens] == websocket:
                ActiveTokens.pop(tokens)
                authSuccess.remove(websocket)
    connectedUsers.remove(websocket)
    if masterSocket == websocket:
        masterSocket = None
        print("Master Logged out!")
    await notify_users(websocket)

async def register(websocket):
    connectedUsers.append(websocket)
    await notify_users(websocket)

async def pinging_event(websocket):
    js = {"Event":"ClientPingEvent","ErrorCode":0}
    js = json.dumps(js)
    await websocket.send(js)
    

async def CheckAuth(token,websocket):
    global authSuccess
    global ActiveTokens
    with open(cd+r'\tokens.json', 'r') as json_file:
        tokens = json.load(json_file)
    if token in tokens['tokens']:
        if token in ActiveTokens:
            js = {"eventType":"Authorization","message":"There is already an active session with this token.","errorCode":1}
            await websocket.send(json.dumps(js))
            return
        ActiveTokens[token] = websocket
        authSuccess.append(websocket)
        js = {"eventType":"Authorization","message":"Auth Success","errorCode":0}
        await websocket.send(json.dumps(js))
        return
    js = {"eventType":"Authorization","message":"Auth Failed, invalid token.","errorCode":2}
    await websocket.send(json.dumps(js))    
    return 
        
def masterEvent():
    pass

async def EventHandling(websocket,message):
    global authSuccess
    if not message.get('eventType'):
        return
    event = message['eventType']
    if event == "Authorization":
        if not message.get('token'):
            js = {"eventType":"Authorization","message":"No token Provided!","errorCode":3}
            await websocket.send(json.dumps(js))    
            return
        await CheckAuth(message['token'],websocket)
        return
    if event =="MasterLogin":
        if not message.get("token"):
            js = {"eventType":"Authorization","message":"No token Provided!","errorCode":3}
            await websocket.send(json.dumps(js))    
            return
        if message['token'] == MasterKey:
            global masterSocket
            print("Master Logged In!")
            js = {"eventType":"Authorization","message":"Auth Success","comments":"Welcome Master, Have a good day!","errorCode":0}
            await websocket.send(json.dumps(js)) 
            masterSocket = websocket
            return
    if event == "MasterSendData" and websocket == masterSocket:
        data = message.get('data')
        dataType = message.get('dataType')
        if data and dataType:
            if dataType == "Authorised":
                members = authSuccess
            else: 
                members = connectedUsers
            for user in members:
                await user.send(json.dumps(data))

async def webserver(websocket, path):
    while True:
        try:
            message = await websocket.recv()
            print(message)
            if message !="start":
                continue
            js = ["newQuestion",{"qid":"5fe49780842397b0a37906a2","number":10,"question":"Name the main lead actor & actress of Eik Main Aur Eik Tu?"}]
            msg = "42"+ json.dumps(js,separators = (",", ":"))
            await websocket.send(msg)
            js = ["options",["Deepika & Imran Khan","Kareen & Akshay Kumar","Deepika & Shahid","Kareena & Imran Khan"]]
            msg = "42"+ json.dumps(js,separators = (",", ":"))
            await websocket.send(msg)
            print("im here")
        except Exception as e:
            print(e)

start_server = websockets.server.serve(webserver, "localhost",1235)#"172.31.45.34", 1235)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
print("Server is up!")