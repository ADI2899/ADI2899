import subprocess
import tkinter as tk
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pyrebase
import time

t_end = time.time() + 60 * 1

firebaseConfig = {
    "apiKey": "AIzaSyDKi09ANqxdxwBgkmocjzNcXkkVjYb3NgQ",
    "authDomain": "fano-595d2.firebaseapp.com",
    "databaseURL": "https://fano-595d2.firebaseio.com",
    "projectId": "fano-595d2",
    "storageBucket": "fano-595d2.appspot.com",
    "messagingSenderId": "984398842850",
    "appId": "1:984398842850:web:9f9605f7e525fe2dedc7bb"
}
firebase = pyrebase.initialize_app(firebaseConfig)
aditya_db = firebase.database()
aditya_db.child("attendance").update({"aditya": False})
aditya_db.child("attendance").update({"vidya": False})



class Attend:
    def __init__(self):

        self.root = tk.Tk()
        self.root.title("STUDENT ATTENDANCE SYSTEM")
        self.root.geometry('600x800')

        self.lable1 = tk.Label(self.root, text="STUDENT ATTENDANCE SYSTEM", relief="groove")
        self.lable1.config(font=('Couier', 20))
        self.lable1.grid(row=0, columnspan=3, padx=150, ipadx=10, ipady=10, pady=10)

        self.button = tk.Button(self.root, text="START", padx=60, pady=20, command=self.start)
        self.button.grid(row=4, column=0, pady=100)

        self.button2 = tk.Button(self.root, text="STOP", padx=60, pady=20)
        self.button2.grid(row=4, column=2, pady=100)

        self.button3 = tk.Button(self.root, text="RECORDED ATTENDANCE", padx=50, pady=20)
        self.button3.grid(row=5, columnspan=3, pady=40)

        self.button4 = tk.Button(self.root, text="EXIT", padx=50, pady=20, command=self.quit)
        self.button4.grid(row=6, columnspan=3, pady=20)
        self.root.mainloop()

    def quit(self):
        self.root.destroy()

    def start(self):

        path = r'C:\\Users\\ADITYA\\PycharmProjects\\ATTENDANCE_SYSTEM\\Imagesattendance'
        images = []
        classNames = []
        myList = os.listdir(path)
        print(myList)
        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])
        print(classNames)

        def findencodings(images):
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            return encodeList

        def markattendance(name):
            with open("attendance.csv", 'r+') as f:
                myDatalist = f.readlines()
                namelist = []
                for line in myDatalist:
                    entry = line.split(',')
                    namelist.append(entry[0])
                if name not in namelist:
                    now = datetime.now()
                    dtString = now.strftime('%H:%M:%S')
                    f.writelines(f"\n{name},{dtString}")

        encodelistknown = findencodings(images)
        print('Encoding Complete')

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cv2.destroyAllWindows()

        while time.time() < t_end:
            success, img = cap.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facescurframe = face_recognition.face_locations(imgS)
            encodescurframe = face_recognition.face_encodings(imgS, facescurframe)

            for encodeFace, faceLoc in zip(encodescurframe, facescurframe):
                matches = face_recognition.compare_faces(encodelistknown, encodeFace)
                faceDis = face_recognition.face_distance(encodelistknown, encodeFace)
                # print(faceDis)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    print(name)
                    if name == "ADITYA":
                        aditya_db.child("attendance").update({"aditya": True})
                    elif name == "VIDYA":
                        aditya_db.child("attendance").update({"vidya": True})

                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    markattendance(name)

            cv2.imshow('webcam', img)
            cv2.waitKey(1)

    def RecoredAttendance(self):
        subprocess.Popen(["notepad.exe", "C:\\Users\\ADITYA\\PycharmProjects\\ATTENDANCE_SYSTEM\\attendance.csv"])


app = Attend()
