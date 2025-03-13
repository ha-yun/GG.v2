import openai
import os

# .env 파일에서 API 키 직접 읽기
with open(".env") as f:
    for line in f:
        key, value = line.strip().split("=")
        os.environ[key] = value  # 환경 변수로 등록

# 환경 변수에서 API 키 가져오기
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


a = '돌고래'
prompt = f"one celebrity product {a} featuring such as posters, keychains, T-shirts, and albums."


# 달리 모델
def make_image( prompt=prompt):
  res = openai.images.generate(
      model   = "dall-e-3",   # 적용 모델
      prompt  = prompt,       # 프럼프트
      size    = "1024x1024",  # 출력(결과물) 해상도
      quality = "standard",   # 품질
      n       = 1,            # 1개만 생성
  )
  return res

img = make_image( prompt )

# 그림 원본 링크
print( img.data[0].revised_prompt )
image_url = img.data[0].url

print("생성된 이미지:", image_url)
