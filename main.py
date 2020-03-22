import time
import cv2
import sys
import datetime as dt
from time import sleep
import tkinter as tk
import random

cascPath = "frontal_face_model.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
anterior = 0

def facialDetection():
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw a rectangle around the faces
    if len(faces) > 0:
        # Face detected display wrong time
        return True
        updateClock(wrong=True)

    else:
        return False
        updateClock(wrong=False)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    if anterior != len(faces):
        anterior = len(faces)


    # Display the resulting frame
    cv2.imshow('Video', frame)

# When everything is done, release the capture
faceInPreviousFrame = True

def updateClock():
    global faceInPreviousFrame
    face = facialDetection()
    if not face:
        lbl.config(text = time.strftime('%H:%M:%S %p')) 
        faceInPreviousFrame = False
    elif not faceInPreviousFrame:
        hour = random.randint(1,12)
        minute = random.randint(1,59)
        second = random.randint(1,59)

        # Adds 0 infront
        if hour < 10:
            hour = "0" + str(hour)
        
        if minute < 10:
            minute = "0" + str(minute)

        if second < 10:
            second = "0" + str(second)

        amPm = random.choice(["AM", "PM"])
        lbl.config(text = "{}:{}:{} {}".format(hour, minute, second, amPm)) 
        faceInPreviousFrame = True

    lbl.after(10, updateClock)


root = tk.Tk() 
root.title('Clock') 
#root.minsize(1920, 1080)
root.configure(background='black')
root.geometry('1920x1080+0+0')

lbl = tk.Label(root, font = ('calibri', 275, 'bold'), 
    background = 'black', 
    foreground = 'green') 
lbl.config(text = time.strftime('%H:%M:%S %p')) 
lbl.pack(anchor = 'center', fill="none", expand=True)

# facialDetection()
updateClock()
root.mainloop()


# Code to close cv2
video_capture.release()
cv2.destroyAllWindows()