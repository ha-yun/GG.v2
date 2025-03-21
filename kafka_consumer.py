from kafka import KafkaConsumer
import json
from ai_translation import translate_text
from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")

consumer = KafkaConsumer(
    'chat-translations',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id='chat-group'
)

for message in consumer:
    data = message.value

    # target_lang이 없으면 기본값으로 영어("en") 설정
    target_lang = data.get('target_lang', 'en')
    
    translated_msg = translate_text(data['msg'], target_lang)  

    # Kafka에서 번역된 메시지를 받아와 Socket을 통해 클라이언트로 전달
    socketio.emit("translated_message", {
        "room": data['room'],
        "user": data['user'],
        "translated_msg": translated_msg
    })
