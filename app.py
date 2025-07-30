from flask import Flask, render_template, Response, request, redirect, url_for, session
import cv2
import mediapipe as mp
import os
import pyttsx3
import threading
import queue
from gtts import gTTS
import time

app = Flask(__name__)
app.secret_key = os.urandom(24)

users = {}

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

messages = {
    "00000": "Resting Hand",
    "10000": "Thumbs Up",
    "01000": "Pointing",
    "00100": "Middle Finger",
    "00010": "Ring Finger",
    "00001": "Pinky Finger",
    "11000": "L Shape",
    "10100": "Peace Sign",
    "01100": "Gun Sign",
    "10010": "OK Sign",
    "10001": "Rock On",
    "11100": "Three Fingers",
    "01110": "Four Fingers",
    "11110": "Open Hand",
    "01111": "High Five",
    "10101": "Surprise",
    "11010": "I Love You",
    "11111": "Stop",
    "01010": "Victory",
    "00101": "Hang Loose"
}

speech_queue = queue.Queue()

def text_to_speech():
    engine = pyttsx3.init()
    while True:
        message = speech_queue.get()
        if message is None:
            break
        try:
            engine.say(message)
            engine.runAndWait()
        except Exception as e:
            print(f"pyttsx3 error: {e}")
        speech_queue.task_done()

speech_thread = threading.Thread(target=text_to_speech)
speech_thread.daemon = True
speech_thread.start()

@app.route('/')
def home():
    if 'username' in session:
        return render_template('startcam.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        return "Invalid credentials!"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users:
            users[username] = password
            return redirect(url_for('login'))
        return "Username already exists!"
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_frames():
    cap = cv2.VideoCapture(0)
    last_message = ""
    while True:
        success, img = cap.read()
        if not success:
            break

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        
        fingers = {"4": 0, "8": 0, "12": 0, "16": 0, "20": 0}
        message = "Unknown Sign"

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = [(id, int(lm.x * img.shape[1]), int(lm.y * img.shape[0])) for id, lm in enumerate(hand_landmarks.landmark)]
                
                if landmarks:
                    fingers["4"] = 1 if landmarks[4][1] > landmarks[3][1] else 0
                    fingers["8"] = 1 if landmarks[8][2] < landmarks[6][2] else 0
                    fingers["12"] = 1 if landmarks[12][2] < landmarks[10][2] else 0
                    fingers["16"] = 1 if landmarks[16][2] < landmarks[14][2] else 0
                    fingers["20"] = 1 if landmarks[20][2] < landmarks[18][2] else 0
                
                finger_pattern = "".join(str(fingers[key]) for key in ["4", "8", "12", "16", "20"])
                message = messages.get(finger_pattern, "Unknown Sign")

                mp.solutions.drawing_utils.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                cv2.putText(img, message, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if message != last_message:
            speech_queue.put(message)
            last_message = message

        ret, buffer = cv2.imencode('.jpg', img)
        if not ret:
            break
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

if __name__ == '__main__':
    app.run(debug=True)
