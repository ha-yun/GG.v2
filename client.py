import socket
import threading
import speech_recognition as sr
from gtts import gTTS
import os
import time
import playsound

server_host = 'localhost'
server_port = 55555

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 서버와 연결
client_sock.connect((server_host, server_port))
print(f'Server:{server_host},{server_port}와 정상적으로 연결됨')

# 서버 메시지 수신
def receive_messages():
    while True:
        try:
            response = client_sock.recv(1024).decode()
            if not response:
                break
            print(f"\n[서버]: {response}")
            speak(response)  # 응답을 음성으로 변환
        except:
            break

# 클라이언트 메시지 전송
def send_messages():
    while True:
        message = input("[클라이언트 입력]: ")
        if message.lower() == "exit":
            client_sock.close()
            break
        client_sock.sendall(message.encode())

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
