import socket
import threading  # 🔹 threading 모듈 추가
import speech_recognition as sr
from gtts import gTTS
import os
import time
import playsound
host = 'localhost'
port = 55555

parent_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
parent_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

parent_sock.bind((host, port))
parent_sock.listen(5)
print(f'Server:{host},{port}에서 연결 대기 중...')

child_sock, child_addr = parent_sock.accept()
print(f'{child_addr}에서 접속')

# 클라이언트 메시지 수신
def receive_messages():
    while True:
        try:
            message = child_sock.recv(1024).decode()
            if not message:
                break
            print(f"\n[클라이언트]: {message}")
            speak(message)  #응답을 음성으로 변환
        except:
            break

# 서버 메시지 전송
def send_messages():
    while True:
        server_message = input("[서버 입력]: ")
        if server_message.lower() == "exit":
            child_sock.close()
            parent_sock.close()
            break
        child_sock.sendall(server_message.encode())

# 음성 출력 함수 (TTS)
def speak(text):
    tts = gTTS(text=text, lang='ko')
    filename = 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename, True) 
    time.sleep(1)  
    os.remove(filename)  

#스레드 생성 및 실행
receive_thread = threading.Thread(target=receive_messages)
send_thread = threading.Thread(target=send_messages)

receive_thread.start()
send_thread.start()

receive_thread.join()
send_thread.join()
