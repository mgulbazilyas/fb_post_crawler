#! python3
import os
import pyrebase
import time
from subprocess import Popen, PIPE

import threading
def updateFile():
        global storage
        threading.Timer(600.0,updateFile).start()
        storage.child("txt/runner.txt").put("runner.txt")
        download_url = storage.child("txt/runner.txt").get_url('')
        db.child("scripts").update({"runner_file" : download_url})
        
firebaseConfig = {
  'apiKey': "AIzaSyARUhOP1jwlYPURuevEMBYWADP2hwx2X8Q",
  'authDomain': "admin-app-467bf.firebaseapp.com",
  'databaseURL': "https://admin-app-467bf.firebaseio.com",
  'projectId': "admin-app-467bf",
  'storageBucket': "admin-app-467bf.appspot.com",
  'messagingSenderId': "905924835344",
  'appId': "1:905924835344:web:8c32cadfc547830c10f295",
  'measurementId': "G-0NKJW34D2J"

}

firebase = pyrebase.initialize_app(firebaseConfig)
db =  firebase.database()
storage = firebase.storage()

updateFile()

def scriptHandler(message):
        global runnerScript      
        runnerScript = message['data']
        if runnerScript:
                print("Started")
        else:
                print("Stopped")
runnerScript = db.child("scripts").child("runner_script").get()
runnerScript = runnerScript.val()

db.child("scripts").child("runner_script").stream(scriptHandler)

while 1:
    if runnerScript:
       
        os.system('python3 group_crawler.py')
        print("done")
    else:
        time.sleep(5)
