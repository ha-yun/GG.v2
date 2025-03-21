from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room
from translate_service import translate_text

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# ✅ 사용자 정보 저장 (SID 기반)
user_data = {}

@socketio.on("register")
def register_user(data):
    """ 사용자가 접속하면 user_id를 설정 """
    sid = request.sid
    user_id = data.get("user_id", f"guest_{sid[:5]}")  # ✅ 고유 ID 생성

    # ✅ 기존 user_id 중복 확인 후 고유값 부여
    if any(info["user_id"] == user_id for info in user_data.values()):
        user_id = f"{user_id}_{sid[:3]}"  # 중복 발생 시 유니크한 값 추가

    user_data[sid] = {"user_id": user_id, "target_lang": "en"}
    join_room(sid)

    print(f"✅ 새로운 사용자 등록: {user_id} (SID: {sid})")
    emit("registered", {"user_id": user_id}, room=sid)

@socketio.on("set_language")
def set_user_language(data):
    """ 사용자의 번역 언어 변경 """
    sid = request.sid
    target_lang = data.get("target_lang", "en")

    if sid in user_data:
        user_data[sid]["target_lang"] = target_lang
        print(f"✅ {user_data[sid]['user_id']}의 번역 언어 설정: {target_lang}")

@socketio.on("message")
def handle_message(data):
    """ 사용자가 보낸 메시지를 번역 후 모든 사용자에게 전송 """
    sender_sid = request.sid
    message = data["message"]

    if sender_sid not in user_data:
        print("❌ 에러: 등록되지 않은 사용자가 메시지를 전송함")
        return

    sender_id = user_data[sender_sid]["user_id"]
    print(f"📢 서버 메시지 수신: {sender_id}: {message}")

    # ✅ 모든 사용자에게 각자의 번역 언어로 전송 (자신 포함)
    for receiver_sid, info in user_data.items():
        target_lang = info["target_lang"]

        # ✅ 번역 언어가 원본 언어와 동일하면 번역하지 않음
        if target_lang == "auto":
            translated_text = message
        else:
            translated_text = translate_text(message, target_lang=target_lang, method="openai")

        response = {
            "user_id": sender_id,
            "original": message,
            "translated": translated_text,
        }

        print(f"📢 서버 메시지 전송 to {info['user_id']} ({target_lang}): {translated_text}")
        emit("message", response, room=receiver_sid)

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5001, host="0.0.0.0", allow_unsafe_werkzeug=True)
