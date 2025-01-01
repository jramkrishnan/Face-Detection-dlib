# app.py
from flask import Flask, Response, render_template, jsonify
import cv2
from face_recognition_system import FaceRecognitionSystem
import threading
from queue import Queue
import json
import atexit

app = Flask(__name__)

# Global variables
face_system = FaceRecognitionSystem()
recognition_queue = Queue(maxsize=10)
video_capture = None

def initialize_camera():
    global video_capture
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Could not open camera")
        return False
    return True

def cleanup():
    global video_capture
    if video_capture is not None:
        video_capture.release()
    cv2.destroyAllWindows()

atexit.register(cleanup)

def generate_frames():
    global video_capture
    
    if video_capture is None:
        if not initialize_camera():
            return
    
    while True:
        success, frame = video_capture.read()
        if not success:
            break
            
        processed_frame, recognized_names = face_system.process_frame(frame)
        
        if recognized_names:
            try:
                recognition_queue.put(recognized_names, block=False)
            except:
                pass
        
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/recognitions')
def get_recognitions():
    try:
        names = recognition_queue.get_nowait()
        return json.dumps({'names': names})
    except:
        return json.dumps({'names': []})

@app.route('/attendance')
def get_attendance():
    attendance_data = face_system.get_attendance_report()
    return jsonify(attendance_data)

if __name__ == '__main__':
    if initialize_camera():
        print("Camera initialized successfully")
        print("Access the application at http://127.0.0.1:5000")
        app.run(debug=True, use_reloader=False)
    else:
        print("Failed to initialize camera")
