import openai
import os
from deep_translator import GoogleTranslator

# .env 파일에서 API 키 직접 읽기
with open(".env") as f:
    for line in f:
        key, value = line.strip().split("=")
        os.environ[key] = value  # 환경 변수로 등록

# 환경 변수에서 API 키 가져오기
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# OpenAI API 클라이언트 생성
client = openai.OpenAI(api_key=OPENAI_API_KEY)


def translate_text(text, source_lang="auto", target_lang="en", method="openai"):
    """
    텍스트를 번역하는 함수
    - method="google"  -> Google Translate 사용
    - method="openai"  -> OpenAI GPT 사용
    """
    # ✅ 같은 언어면 번역하지 않음
    if source_lang == target_lang:
        return text  # 그대로 반환
    
    # ✅ Google Translator (deep-translator 활용)
    if method == "google":
        try:
            return GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        except Exception as e:
            return f"Google Translate Error: {e}"

    # ✅ OpenAI GPT를 이용한 번역
    elif method == "openai":
        try:
            # target_lang을 프롬프트 내부에서 명확하게 설정
            prompt = (
                f"You are a professional translator. "
                f"Translate the following text into {target_lang}. "
                f"DO NOT change the meaning, DO NOT paraphrase, DO NOT add explanations. "
                f"ONLY return the translated text in {target_lang}, without any additional commentary. "
                f"Make sure the response is 100% in {target_lang}, with no English or other languages mixed in."
            )

            response = client.chat.completions.create(
                model="gpt-4o-mini", 
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.0  # ✅ 변형 없이 직역하도록 설정
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"OpenAI Translation Error: {e}"

    return text


# ✅ 테스트 코드 (직접 실행 시 확인 가능)
#if __name__ == "__main__":
#    print(translate_text("안녕하세요!", target_lang="en", method="google"))  # Google 번역
#    print(translate_text("안녕하세요!", target_lang="en", method="openai"))  # OpenAI 번역