from logging import StreamHandler
import firebase_admin
from firebase_admin import db

cred = firebase_admin.credentials.Certificate('itadori22.json')
firebase_admin.initialize_app(cred, {'databaseURL':'https://itadori22-682d7-default-rtdb.europe-west1.firebasedatabase.app/'})
ref = firebase_admin.db.reference('/')

newMessage = {'name': 'Johannes', 'text': 'hello world'}    
messages_stream = ref.child('messages').listen(StreamHandler)    
ref.child('messages').push(newMessage)

