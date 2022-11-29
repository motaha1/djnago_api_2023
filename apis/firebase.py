import pyrebase

firebaseConfig = {
  'apiKey': "AIzaSyBieYFF0MbSnxRde82anPnkxJ4jyriAz2o",
  'authDomain': "gradproject-6d49d.firebaseapp.com",
 'projectId': "gradproject-6d49d",
  'storageBucket': "gradproject-6d49d.appspot.com",
  'messagingSenderId': "762585809218",
  'appId': "1:762585809218:web:c1918968e3ede4256588db",
  'measurementId': "G-C94BX84X6Z" , 
  "databaseURL": ""

}


firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()


def firebase_sigup (email ,password):
   
        auth.create_user_with_email_and_password(email ,password)

firebase_sigup("mo1@mo.com" , "fffffff")