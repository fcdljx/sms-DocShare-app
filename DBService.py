from flask import Flask
from flask import render_template
from flask import Response, request, jsonify

import json
import time

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate("./key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

doc_ref = db.collection(u'users').document(u'alovelace')

# code is the session ID
def get_all(code):
    res = ''
    doc_ref = db.collection(u'sessions').document(code).collection(u'messages')
    docs = doc_ref.stream()
    for doc in docs:
        res += f"{doc.to_dict()['text']}\n"
        print(f'{doc.id} => {doc.to_dict()}')
    return res


def create_new(code, id, sender, text):
    doc_ref = db.collection(u'sessions').document(code).collection(u'messages').document(id)
    data = {
        u'from': sender,
        u'text': text
    }
    doc_ref.set(data)

    return get_all(code)

# Display dashboard
@app.route("/dashboard", methods=['GET', 'POST'])
#get all user data here
def dashboard():
    docs = db.collection('sessions').stream()
    items = []
    for doc in docs:
        data = doc.to_dict()
        data['id'] = doc.id
        items.append(data)

    return render_template("dashboard.html", items=items)

# Display single sessions
@app.route("/display_user_data/<session_id>",methods=['GET', 'POST'])
# @app.route("/display_user_data",methods=['GET', 'POST'])
def display_user_data(session_id):
    # get data for one user
    session_id = session_id.replace("<","").replace(">","")
    docs = db.collection('sessions').document(str(session_id)).collection("messages").stream()
    messages = []
    for m in docs:
        msg = m.to_dict()
        messages.append(msg)
        print(msg)
    return render_template("display_session_data.html", session_id = session_id, items = messages)

if __name__ == "__main__":
    app.run(debug=True)
