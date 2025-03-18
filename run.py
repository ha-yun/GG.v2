# 1. 필요한 모듈 가져오기
# Flask 관련 모듈
from flask import Flask, jsonify, request, render_template  # Flask 관련 모듈

# OpenAI API 사용
import openai

# Llama-Index 관련 모듈
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Document
from llama_index.core import GPTVectorStoreIndex

# HTTP 요청 처리
import requests  

# 환경 변수 관리
import os



# 2. Flask 앱 초기화
app = Flask(__name__)  # "__main__"  # Flask 애플리케이션 생성

# .env 파일에서 API 키 직접 읽기
with open(".env") as f:
    for line in f:
        key, value = line.strip().split("=")
        os.environ[key] = value  # 환경 변수로 등록

# 환경 변수에서 API 키 가져오기
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# 기존 프로젝트의 msa-starboard 모듈에서 생성된 데이터를 활용하여 로드
def collect_data():
    url = "http://localhost:8080/api/posts"  # 'msa-starboard'-'모든 게시글 조회' URL / 현재는 로컬에서 가능(실제 서비스 URL로 변경해야 함)
    response = requests.get(url)
    data = response.json()
    return [Document(text=f"{post['title']}\n\n{post['content']}") for post in data]

documents = collect_data()

# 인덱스 생성
index = GPTVectorStoreIndex.from_documents( documents )

# 엔진 생성
query_engine = index.as_query_engine()



# 3. 라우팅 처리
#    홈페이지 구성
@app.route('/') # URL, method 지정
def home():
    return "llama-index, openai, LLM service"

#    LM에 질의하는 쿼리(restful api 구성)
#    http://127.0.0.1:5000/query
@app.route( '/query', methods=['POST', 'GET'] )
def query():
    if request.method == 'POST':
        # 사용자가 입력한 프럼프트(질문) 획득
        question = request.json.get('question')
        print( question )

        # 프롬프트(질문)에 한국어로 요청/실제 star가 답변하는 것처럼 요청 추가
        korean_prompt = f"질문: { question }\n\n답변을 한국어로 작성해주세요. 그리고 답변을 실제 K-pop 여자아이돌이 말하는 것처럼 작성해주세요"
        response = query_engine.query( korean_prompt )

        # 응답을 문자열로 변환
        answer = str( response )
        return jsonify({"answer": answer})
    else:
        # html 화면 구성
        return render_template( 'query.html' )



# 4. 서버가동
if __name__ == '__main__': # 엔트리포인트(코드의 진입로,시작점)
    app.run(debug=True)