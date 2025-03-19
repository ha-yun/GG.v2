# 1. 필요한 모듈 가져오기 => Jinja2 템플릿 엔진
from flask import Flask, jsonify, request, render_template, send_from_directory

# jsonify: JSON 응답용
# request : 사용자 전달 데이터 획득용
import os
import requests
from datetime import datetime
from CreateGoods import retrieve_goods, generate_image_prompt, generate_image  # 모델 로드

# 2. Flask 앱 초기화
app = Flask(__name__)   # "__main__"


# 절대 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/goods_image/<string:filename>')
def serve_image(filename):
    print(f"📂 요청된 파일: {filename}")  # 요청된 파일명이 출력되는지 확인
    return send_from_directory(os.path.join(BASE_DIR, 'goods_image'), filename)


# 3. 라우팅 처리
@app.route('/')     # URL, method 지정 (기본값 get방식)
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/goods', methods=['GET'])
def goods():
    return render_template('goods.html')

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
    # 저장 경로 생성
    save_path = f"./goods_image/{timestamp}.jpg"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)  # 폴더 없으면 생성

    # 이미지 데이터 다운로드 후 저장
    img_response = requests.get(image_url)  # 이미지 다운로드
    if img_response.status_code == 200:  # 요청 성공 확인
        with open(save_path, "wb") as file:
            file.write(img_response.content)
        print(f"✅ 이미지 저장 완료: {save_path}")
    else:
        print(f"❌ 이미지 다운로드 실패! 상태 코드: {img_response.status_code}")
        return jsonify({'error': '이미지 다운로드 실패'}), 500
    
    # 🔥 추가된 부분: 이전 프로젝트(GG-SB) API 호출 - 커스텀 굿즈 저장
    api_url = "http://52.77.19.120:8080/customgoods/save"  # 기존 프로젝트의 API URL
    payload = {
        "customgoodsName": timestamp,  # 원하는 값
        "customgoodsDescription": user_input,
        "customgoodsImageUrl": save_path  # 저장된 이미지 경로
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"✅ 기존 서버에 저장 완료! 응답: {response.json()}")
        else:
            print(f"❌ 기존 서버 저장 실패! 상태 코드: {response.status_code}, 응답: {response.text}")
    except Exception as e:
        print(f"🚨 API 요청 중 오류 발생: {e}")


    response_data = {'answer': '이미지 생성 완료!', 'image_url': save_path}
    return jsonify(response_data)


# 4. 서버가동
if __name__ == '__main__':  # 엔트리포인트(코드의 진입로, 시작점)
    app.run(debug=True)
