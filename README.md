# ✋ SignSpeak - Real-Time Sign Language Interpreter

**SignSpeak** is a real-time sign language interpreter built using Flask, OpenCV, and MediaPipe. It detects hand gestures through a webcam, translates them into meaningful text labels, and speaks the interpreted signs aloud, making communication smoother between the deaf community and the hearing world.

## 🚀 Features

- 🔐 User Registration & Login System
- 📷 Live Webcam-Based Gesture Detection
- 🖐️ Recognizes 20+ Common Hand Signs
- 🗣️ Converts Detected Signs to Speech (using `pyttsx3` or `gTTS`)
- 💬 Real-time Display of Predicted Gesture
- 🌐 Web Interface Built with Flask & Jinja Templates

## 🧠 Core Technologies

- **Python**
- **Flask** – Web framework for user authentication and routing
- **OpenCV** – Captures and processes webcam video
- **MediaPipe Hands** – Detects hand landmarks for gesture recognition
- **Text-to-Speech** – `pyttsx3` engine to vocalize recognized signs
- **Threading & Queues** – Ensures non-blocking speech synthesis

## 📁 Folder Structure

```
SignSpeak/
│
├── templates/
│   ├── login.html
│   ├── register.html
│   └── startcam.html
│
├── app.py                # Main Flask application
├── README.md             # You're reading it!
```

## 🧪 Recognized Gestures

| Binary Finger Pattern | Gesture         |
|------------------------|----------------|
| `10000`               | Thumbs Up       |
| `01000`               | Pointing        |
| `11110`               | Open Hand       |
| `11010`               | I Love You      |
| `10100`               | Peace Sign      |
| `01100`               | Gun Sign        |
| `10010`               | OK Sign         |
| ...                   | And many more!  |

*Each digit represents a finger (thumb to pinky), with `1` = extended, `0` = folded.*

## 📦 Setup & Run

### 🔧 Requirements

- Python 3.x
- Webcam
- Virtual environment (recommended)

### 🔌 Installation

```bash
git clone https://github.com/yourusername/signspeak.git
cd signspeak
pip install -r requirements.txt
python app.py
```

Visit `http://127.0.0.1:5000` on your browser.

> Make sure your webcam permissions are enabled in your browser/system.

### 🛠 Sample `requirements.txt`

```
flask
opencv-python
mediapipe
pyttsx3
gtts
```

## 📸 Demo

> *[Insert a GIF or Screenshot of your app in action]*  
> *(Optional but HIGHLY recommended!)*

## 🧠 How It Works

- MediaPipe detects 21 hand landmarks in real time.
- Finger extension is calculated using geometric comparison of landmark positions.
- Each combination is mapped to a predefined gesture.
- The gesture is printed and converted to speech using a background thread.

## 🛡 License

This project is licensed under the [MIT License](LICENSE).

---

### ✨ Made with purpose — to bridge the communication gap, one sign at a time.
