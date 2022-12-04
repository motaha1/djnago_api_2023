
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("Key.json")
firebase_admin.initialize_app(cred)


db = firestore.client()


def addpatient_firestore(email , name , city  ):
    db.collection('Paient').document(email).set({ 'name':name , 'city' :city })


