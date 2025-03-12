from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import speech_recognition as sr
from gtts import gTTS
import os
import time
import playsound

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # WebSocket 

# 음성 출력 함수 (TTS)
def speak(text):
    tts = gTTS(text=text, lang='ko')
    filename = 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename, True)
    time.sleep(1)
    os.remove(filename)

# 클라이언트가 메시지를 보낼 때
@socketio.on("send_message")
def handle_message(data):
    print(f"[클라이언트]: {data['message']}")
    emit("receive_message", {"message": data["message"]}, broadcast=True)
    speak(data["message"])  # TTS 음성 출력

@app.route("/")
def index():
    return render_template("chat.html")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
