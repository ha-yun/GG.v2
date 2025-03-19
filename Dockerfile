# 1. 베이스 이미지 선택 (Python 3.9 사용)
FROM python:3.9

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 필요한 파일 복사
COPY . /app

# 4. 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 5. Flask 앱 실행 (Gunicorn 사용)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "run:app"]
