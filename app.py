from flask import Flask, request, jsonify
from kafka_service import send_to_kafka

app = Flask(__name__)

@app.route("/send", methods=["POST"])
def send_message():
    """
    사용자가 채팅 메시지를 보내면 Kafka에 저장하는 API
    """
    data = request.json
    user_id = data.get("user_id", "guest")
    message = data["message"]
    target_lang = data.get("target_lang", "en")

    # Kafka에 저장
    send_to_kafka(user_id, message, target_lang)

    return jsonify({"status": "success", "message": "Message sent to Kafka"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
