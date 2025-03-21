import mysql.connector

# MySQL 연결 설정
db_config = {
    "host": "localhost",
    "user": "root",  # MySQL 사용자명
    "password": "p1234",  # MySQL 비밀번호
    "database": "chat_db"  # 사용할 데이터베이스명
}

# DB 연결 함수
def get_connection():
    return mysql.connector.connect(**db_config)

# 메시지 저장 함수
def save_message(user, msg, room, translated_msg=None):
    """ 채팅 메시지를 MySQL DB에 저장하는 함수 """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO chat_messages (user, msg, room, translated_msg)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (user, msg, room, translated_msg))
        conn.commit()
    except Exception as e:
        print(f"❌ DB 저장 오류: {e}")
    finally:
        cursor.close()
        conn.close()

# 특정 채팅방의 채팅 기록 조회 함수
def get_chat_history(room):
    """ 특정 채팅방의 채팅 기록을 MySQL에서 불러오는 함수 """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT user, msg, room, translated_msg FROM chat_messages WHERE room = %s"
        cursor.execute(query, (room,))
        chat_history = cursor.fetchall()
        return chat_history
    except Exception as e:
        print(f"❌ DB 조회 오류: {e}")
        return []
    finally:
        cursor.close()
        conn.close()
