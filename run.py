# 1. 필요한 모듈 가져오기
from flask import Flask, jsonify, request, render_template
# jsonify: JSON 응답용
# request : 사용자 전달 데이터 획득용

# LLM 기반 RAG 서비스를 위한 패키지 추가
import openai
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Document, GPTVectorStoreIndex


# 2. Flask 앱 초기화
app = Flask(__name__)   # "__main__"

# 2-1. openai-key 설정 -> 편의상 키 설정 -> github업로드 금지
openai.api_key = ''
# 2-2. RAG용 외부 데이터 로드
documents = SimpleDirectoryReader('./data').load_data()
# 위코드는 벡터 디비에서 가져오기 혹은 저장된 인덱스로부터 로드하기 하면 변경가능함
# 2-3. 인덱스 생성
index = GPTVectorStoreIndex.from_documents(documents)
# 2-4. 엔진 생성
# query_engine = index.as_query_engine()


# 3. 라우팅 처리
@app.route('/')     # URL, method 지정 (기본값 get방식)
def home():
    return "llama-index, openai, LLM service"



# 4. 서버가동
if __name__ == '__main__':  # 엔트리포인트(코드의 진입로, 시작점)
    app.run(debug=True)
