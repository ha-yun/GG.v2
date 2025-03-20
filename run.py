# 1. 필요한 모듈 가져오기
from flask import Flask, jsonify, request, render_template, send_from_directory, send_file
import os
import requests
import threading
import time
import torch
import numpy as np
import scipy.io.wavfile as wav
from datetime import datetime
from transformers import AutoProcessor, MusicgenForConditionalGeneration
from flask_socketio import SocketIO, emit, join_room
from gtts import gTTS
import playsound
from CreateGoods import retrieve_goods, generate_image_prompt, generate_image  # 모델 로드

# 2. Flask 앱 초기화
app = Flask(__name__, template_folder="templates")
app.config["SECRET_KEY"] = "secret!"

# WebSocket 설정
socketio = SocketIO(app, cors_allowed_origins="*")  # WebSocket 

# 절대 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# MusicGen 모델 로드 (한 번 다운로드하면 캐시됨)
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")

# 3. 라우트 설정
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/goods')
def goods():
    return render_template('goods.html')

@app.route('/goods_image/<string:filename>')
def serve_image(filename):
    print(f"📂 요청된 파일: {filename}")  # 요청된 파일명이 출력되는지 확인
    return send_from_directory(os.path.join(BASE_DIR, 'goods_image'), filename)

@app.route('/api/ai/goods', methods=['POST'])
def create_goods():
    user_input = request.json.get('user_input')
    retrieved_nodes = retrieve_goods(user_input)
    optimized_prompt = generate_image_prompt(user_input, retrieved_nodes)
    print(f"🎨 생성된 이미지 프롬프트: {optimized_prompt}")
    image_url = generate_image(optimized_prompt)
    print(f"🖼️ 생성된 이미지 URL: {image_url}")

    # 현재 시간 가져오기
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = f"./goods_image/{timestamp}.jpg"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # 이미지 데이터 다운로드 후 저장
    img_response = requests.get(image_url)
    if img_response.status_code == 200:
        with open(save_path, "wb") as file:
            file.write(img_response.content)
        print(f"✅ 이미지 저장 완료: {save_path}")
    else:
        print(f"❌ 이미지 다운로드 실패! 상태 코드: {img_response.status_code}")
        return jsonify({'error': '이미지 다운로드 실패'}), 500

    return jsonify({'answer': '이미지 생성 완료!', 'image_url': save_path})

@app.route("/song")
def song_page():
    return render_template("song.html")

@app.route("/generate", methods=["POST"])
def generate_music():
    try:
        data = request.get_json()
        user_prompt = data.get("style", "default music")

        # 사용자 입력을 텍스트 프롬프트로 변환
        inputs = processor(
            text=[user_prompt],
            padding=True,
            return_tensors="pt",
        )

        # 모델을 사용해 음악 생성
        with torch.no_grad():
            audio_values = model.generate(
                **inputs,
                do_sample=True,
                guidance_scale=3,
                max_new_tokens=512
            )

        # 생성된 오디오 데이터를 NumPy 배열로 변환
        audio_array = audio_values.cpu().detach().numpy()
        sampling_rate = model.config.audio_encoder.sampling_rate

        # WAV 파일로 저장
        filename = f"musicgen_{user_prompt.replace(' ', '_')}.wav"
        output_path = os.path.join("generated_music", filename)
        os.makedirs("generated_music", exist_ok=True)
        wav.write(output_path, rate=sampling_rate, data=audio_array[0, 0])

        return jsonify({"success": True, "filepath": f"/download/{filename}"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/download/<filename>")
def download_file(filename):
    file_path = os.path.join("generated_music", filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"success": False, "error": "파일이 존재하지 않습니다."})

@app.route("/tts")
def chat_page():
    return render_template("chat.html")

# TTS 기능
def speak(text):
    tts = gTTS(text=text, lang="ko")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename, True)
    time.sleep(1)
    os.remove(filename)

# WebSocket 이벤트 핸들러 (채팅 기능)
@socketio.on("join_room")
def handle_join_room(data):
    room = data["room"]
    join_room(room)
    emit("room_messages", {"messages": []}, room=room)  # 초기 메시지 없음

@socketio.on("send_message")
def handle_message(data):
    room = data["room"]
    message = data["message"]

    emit("receive_message", {"message": message}, room=room)

    tts_thread = threading.Thread(target=speak, args=(message,))
    tts_thread.start()

# 4. 서버 실행
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
