import random
from flask import Flask, request, session, Response,jsonify
from flask import render_template
from smsService import send_message
from twilio.twiml.messaging_response import MessagingResponse
from prompts import prompts
from DBService import get_all, create_new

import json
import time

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route("/")
def index():
    return 'hello'


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    body = request.values.get('Body', None)
    sender_number = request.values.get('From', None)
    messageID = request.values.get('MessageSid', None)

    command = body.partition(' ')[0]
    content = body.partition(' ')[2]

    resp = MessagingResponse()

    if command == 'START':
        code = random.randint(100, 500)
        session[sender_number] = code
        send_message(resp, request, prompts['Welcome']+str(code), session)

    elif command == 'JOIN':
        if sender_number in session.keys():
            send_message(resp, request, prompts['DuplicateSession'], session)
        else:
            session[sender_number] = content

    elif command == "READ":
        if sender_number in session.keys():
            send_message(resp, request, get_all(str(session[sender_number])), session)
        else:
            # Todo: send error
            send_message(resp, request, prompts['JoinNotice'], session)

    elif command == 'ADD':
        if sender_number in session.keys():
            res = create_new(str(session[sender_number]), messageID, sender_number, content)
            send_message(resp, request, res, session)

    elif command == 'BYE':
        if sender_number in session.keys():
            session.pop(sender_number)
            send_message(resp, request, 'Bye!', session)
        else:
            send_message(resp, request, prompts['404'], session)


    print(f'sent from {sender_number} with id {messageID} that says {body}')
    return str(resp)
