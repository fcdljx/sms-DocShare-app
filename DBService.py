import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

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
