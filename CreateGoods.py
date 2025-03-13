import numpy as np
import openai
import os
# LlamaIndex 관련 패키지 임포트
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.query_engine import RetrieverQueryEngine

# .env 파일에서 API 키 직접 읽기
with open(".env") as f:
    for line in f:
        key, value = line.strip().split("=")
        os.environ[key] = value  # 환경 변수로 등록

# 환경 변수에서 API 키 가져오기
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


# # 0️⃣ 사용자 검색어 입력
# user_query = "돌고래 문양"

def retrieve_goods(user_query):
    # 1️⃣ Hugging Face 임베딩 모델 로드
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 2️⃣ 데이터 로드
    documents = SimpleDirectoryReader("./data").load_data()

    # 문서를 문장 단위로 분할
    parser = SentenceSplitter(chunk_size=100, chunk_overlap=20)  # 100 토큰씩 분할

    # 4️⃣ 문서를 Chunk 단위로 변환 후 벡터화
    nodes = parser.get_nodes_from_documents(documents)
        
    index = VectorStoreIndex(nodes, embed_model=embed_model)

    # 5️⃣ 검색 엔진 생성 (문서 내부 내용 검색)
    query_engine = RetrieverQueryEngine.from_args(index.as_retriever())

    # 7️⃣ 검색어와 가장 유사한 내용 찾기
    retrieved_nodes = query_engine.retrieve(user_query)
    return retrieved_nodes


# 🔹 GPT를 이용해 이미지 프롬프트 생성
def generate_image_prompt(user_input, retrieved_nodes):
    prompt = f"""
    사용자의 요청: {user_input}
    관련 문서 내용: {retrieved_nodes}
    
    위 내용을 기반으로 DALL·E 3에서 적절한 이미지를 생성할 수 있는 프롬프트를 만들어 주세요.  
    단, 생성되는 이미지는 실제 상품 목업(mockup)처럼 보이도록 하고, 굿즈에 이미지가 적용된 모습을 포함해야 합니다.
    """
    response = openai.chat.completions.create(
        model="gpt-4o-mini", # 질의당 0.15달러
        messages=[{"role": "system", "content": "이미지 생성에 최적화된 프롬프트를 생성해 주세요."},
                  {"role": "user", "content": prompt}],
        max_tokens=100
    )
    
    return response.choices[0].message.content


# # 🔹 GPT-4를 이용한 이미지 프롬프트 생성 확인
# retrieved_nodes = retrieve_goods(user_query)
# optimized_prompt = generate_image_prompt(user_query, retrieved_nodes)
# print(f"🎨 생성된 이미지 프롬프트: {optimized_prompt}")

# 🔹 DALL·E 3를 이용해 이미지 생성
def generate_image(prompt):
    response = openai.images.generate(
        model="dall-e-3",
        prompt=prompt,
        quality = "standard",   # 품질
        n       = 1,
        size="1024x1024"
    )
    return response.data[0].url


# # 🔹 DALL·E 3를 이용한 이미지 생성 확인
# image_url = generate_image(optimized_prompt)
# print(f"🖼️ 생성된 이미지 URL: {image_url}")