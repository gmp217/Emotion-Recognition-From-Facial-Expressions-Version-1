from json.tool import main
import cv2
from flask import redirect
from model import FacialExpressionModel
import numpy as np
import sys
import time
from flask import Flask, redirect, render_template, Response, request
import cgi, os
from pathlib import Path
from keras.preprocessing.image import img_to_array

import cv2
import time
import script

facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model = FacialExpressionModel("model.json", "model_weights.h5")
font = cv2.FONT_HERSHEY_SIMPLEX
#path=Path(r'C:\Users\medha\Documents\major project\fn.mp4')
path = Path(r'E:\Users\mp\Project 3\fn.mp4')
app = Flask(__name__)

class VideoCamera(object):
    
    def __init__(self):
        #self.video = cv2.VideoCapture(r'C:\Users\medha\Downloads\emotions.mp4')
            self.video = cv2.VideoCapture(str(path))
            #self.video = cv2.VideoCapture(r'E:\Users\mp\Project 2\fn.mp4')

    # returns camera frames along with bounding boxes and predictions
        

    def get_frame(self):
        while(self.video.isOpened()):
            _, fr = self.video.read()
            gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
            faces = facec.detectMultiScale(gray_fr, 1.3, 5)

            for (x, y, w, h) in faces:
                fc = gray_fr[y:y+h, x:x+w]

                roi = cv2.resize(fc, (48, 48),interpolation=cv2.INTER_AREA)
                pred = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])
                label_position = (x,y)
                cv2.putText(fr, pred,label_position,cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),3)
                cv2.rectangle(fr,(x,y),(x+w,y+h),(255,0,0),2)

            _, jpeg = cv2.imencode('.jpg', fr)
            return jpeg.tobytes()
        self.cap.release()
        cv2.destroyAllWindows()
        script.re()

    def __del__(self):
        self.video.release()
        cv2.destroyAllWindows()
        if cv2.waitKey(1) & 0xFF == ord('q'):
                return redirect('http://192.168.0.16:5001/')
        #if os.path.exists(r'C:\Users\medha\Documents\major project\fn.mp4'):
            #os.remove(r'C:\Users\medha\Documents\major project\fn.mp4')
        if os.path.exists(r"E:\Users\mp\Project 3\fn.mp4"):
            os.remove(r"E:\Users\mp\Project 3\fn.mp4")