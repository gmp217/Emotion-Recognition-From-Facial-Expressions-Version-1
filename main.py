from flask import Flask, redirect, render_template, Response, request
from camera import VideoCamera,path
from flask import * 
import cv2
from PIL import Image
from script import *

import cgi, os,cgitb
from datetime import datetime
from werkzeug.serving import run_simple

cgitb.enable()
form = cgi.FieldStorage()
app = Flask(__name__)


@app.route('/' ,methods = ['GET','POST'])
def index():
    
        cv2.destroyAllWindows()
        if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
        if os.path.exists(r"E:\Users\mp\Project 2\fn.mp4"):
            cv2.waitKey(0)
            os.unlink(r"E:\Users\mp\Project 2\fn.mp4")
            os.remove(r"E:\Users\mp\Project 2\fn.mp4")
        return render_template('index.html')

@app.route('/insert.html', methods = ['GET','POST'])
def insert():
        return render_template('insert.html')

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
        
        if request.method == 'POST':  
            f = request.files['file']  
            f.filename='fn.mp4'
            f.save(f.filename)  
            return redirect('i.html')     

            #file will be uploaded and saved in the project folder
        #return 'file uploaded successfully'

@app.route('/i.html', methods = ['GET','POST'])
def i():
        return render_template('i.html')

@app.route('/my-link/', methods = ['GET','POST'])
def my_link():
        cv2.destroyAllWindows()
        if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
        return redirect('http://192.168.0.16:5001/')
        
def gen(camera):
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
        return Response(gen(VideoCamera()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.debug=True
    app.run('0.0.0.0', port=5001) 
    #app.run(host='0.0.0.0', debug=True,use_reloader=True)
    