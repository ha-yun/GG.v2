# 1. 필요한 모듈 가져오기
from flask import Flask, jsonify, request, render_template
# jsonify: JSON 응답용
# request : 사용자 전달 데이터 획득용

from CreateGoods import retrieve_goods, generate_image_prompt, generate_image  # 모델 로드


# 2. Flask 앱 초기화
app = Flask(__name__)   # "__main__"

# 3. 라우팅 처리
@app.route('/')     # URL, method 지정 (기본값 get방식)
def home():
    return "llama-index, openai, LLM service"

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

    response_data = {'answer': '이미지 생성 완료!', 'image_url': image_url}
    return jsonify(response_data)


# 4. 서버가동
if __name__ == '__main__':  # 엔트리포인트(코드의 진입로, 시작점)
    app.run(debug=True)
