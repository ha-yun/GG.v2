from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import threading
import os
import time
import playsound
from gtts import gTTS
    
from kafka_service import send_to_kafka



app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")  # WebSocket 

rooms = {}  # 채팅방 저장용 딕셔너리

@app.route("/tts")
def index():
    return render_template("chat.html")

@app.route("/rooms")
def get_rooms():
    return jsonify({"rooms": list(rooms.keys())})

@app.route("/delete_room", methods=["DELETE"])
def delete_room():
    room = request.args.get("room")
    if room in rooms:
        del rooms[room]
        return jsonify({"message": f"채팅방 '{room}' 삭제됨"})
    return jsonify({"error": "채팅방이 존재하지 않음"}), 404

# TTS 기능: 음성을 생성하고 재생하는 함수
def speak(text):
    tts = gTTS(text=text, lang="ko")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename, True)
    time.sleep(1)  # 음성이 끝날 때까지 대기
    os.remove(filename)  # 파일 삭제

# 채팅방 입장 이벤트
@socketio.on("join_room")
def handle_join_room(data):
    room = data["room"]
    join_room(room)
    if room not in rooms:
        rooms[room] = []
    emit("room_messages", {"messages": rooms[room]}, room=room)

# 메시지 수신 및 음성 출력
@socketio.on("send_message")
def handle_message(data):
    room = data["room"]
    message = data["message"]
    
    if room in rooms:
        rooms[room].append(message)
    
    emit("receive_message", {"message": message}, room=room)
    
    # TTS 실행 (별도 스레드로 실행)
    tts_thread = threading.Thread(target=speak, args=(message,))
    tts_thread.start()



@app.route("/send", methods=["POST"])
def send_message():
    """
    사용자가 채팅 메시지를 보내면 Kafka에 저장하는 API
    """
    data = request.json
    user_id = data.get("user_id", "guest")
    message = data["message"]
    target_lang = data.get("target_lang", "en")

    # Kafka에 저장
    send_to_kafka(user_id, message, target_lang)

    return jsonify({"status": "success", "message": "Message sent to Kafka"}), 200

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)

