from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_to_kafka(msg, user, room, target_lang="en"):
    data = {'msg': msg, 'user': user, 'room': room, 'target_lang': target_lang}
    producer.send('chat-translations', value=data)
    producer.flush()  # 즉시 메시지를 전송하도록 강제
