#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from argparse import ArgumentParser
from flask import Flask, request, abort
import requests
import json

import botCmd

# We need this so LINE accepts our API call
access_token = os.getenv('ACCESS_TOKEN', None)

if access_token is None:
    print('Specify ACCESS_TOKEN as environment variable.')
    sys.exit(1)

if os.getenv('FLAG', None) is None:
    print('Specify FLAG as environment variable.')
    sys.exit(1)

if os.getenv('SERVER_INFO', None) is None:
    print('Specify SERVER_INFO as environment variable.')
    sys.exit(1)

botCmd.init()
app = Flask("Hack-me-bot")

def _lineSendMsg(message, replyToken):
    # Make a POST Request to Messaging API to reply to sender
    global access_token
    url = "https://api.line.me/v2/bot/message/reply"
    data = {"replyToken": replyToken,
            "messages": [
            {   "type": "text",
                "text": message
            }]
		   }
    headers = { "Content-Type": "application/json",
                "Authorization": "Bearer %s" % (access_token)
              }
    r = requests.post(url, json=data, headers=headers)

@app.route("/callback", methods=['POST'])
def callback():
    try:
        content = request.json
        message = content["events"][0]["message"]["text"]
        userId = content["events"][0]["source"]["userId"]
        ret_msg = botCmd.runCmd(message, userId)

        if ret_msg == None or ret_msg == "":
            return 'Ok'

        replyToken = content["events"][0]["replyToken"]
        _lineSendMsg(ret_msg, replyToken)
        return 'Ok'
    except:
        return 'Incorrect data'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
