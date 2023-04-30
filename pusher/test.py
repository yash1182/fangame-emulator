import time
import requests
import json
import websocket
import threading
from dhooks import Embed, Webhook
from urllib.parse import quote
import pusher
from flask import Flask, request
from flask_pusher import Pusher


pusher_client = pusher.Pusher(
  app_id='1143299',
  key='4e18031f10c6e628d4fc',
  secret='237716056f391eb6b192',
  cluster='ap2',
  ssl=True
)


app = Flask(__name__)

@app.route("/pusher/auth", methods=['POST'])
def pusher_authentication():
    auth = pusher_client.authenticate(
    channel=request.form['channel_name'],
    socket_id=request.form['socket_id'])
    return json.dumps(auth)

if __name__ == "__main__":
    app.run(debug=True)
    #pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})