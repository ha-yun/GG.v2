# 1. 필요한 모듈 가져오기
from flask import Flask, jsonify, request, render_template
# jsonify: JSON 응답용
# request : 사용자 전달 데이터 획득용

# # LLM 기반 RAG 서비스를 위한 패키지 추가
# import openai
# from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
# from llama_index.core import Document, GPTVectorStoreIndex


# 2. Flask 앱 초기화
app = Flask(__name__)   # "__main__"



# 3. 라우팅 처리
@app.route('/')     # URL, method 지정 (기본값 get방식)
def home():
    return "llama-index, openai, LLM service"



# 4. 서버가동
if __name__ == '__main__':  # 엔트리포인트(코드의 진입로, 시작점)
    app.run(debug=True)
