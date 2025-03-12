# GG.v2

- 파이썬 기반 AI 웹서비스중 Restful 서비스
    - 요청/응답 : json
- 환경구성
    - 가상환경 구축 -> 로컬 개발 (가상환경구성 충돌 방지함)

<details>
<summary>환경구성(기본)</summary>

    ```
        # 터미널 오픈 - 가상환경 web 생성
        python -m venv web
        # 가상환경 진입
            ## 윈도우
            . ./web/Scripts/activate
            ## 맥
            source ./web/bin/activate
        # (가상환경명)프럼프트>
        # 패키지 설치
            pip install flask llama-index openai
    ```
</details>

### ✅ 동일한 환경 세팅하는 방법
- 현재 가상환경에 설치된 패키지 목록 => requirements.txt 파일 이용
    ```
        python -m venv web  # 가상환경 생성

        ## 가상 환경 활성화!!
        source web/bin/activate  # (맥/Linux)
        .\web\Scripts\activate  # (윈도우)
        
        pip install -r requirements.txt  # 패키지 설치
    ```

    - 패키지 추가 설치시, 현재 설치된 패키지를 requirements.txt로 저장(최신 목록 유지!!)
    ```
        pip freeze > requirements.txt
    ```


- 코드 실행
    - (web) ..> python run.py
    - tts 채팅 실행 시 : python app.py -> http://127.0.0.1:5000 접속