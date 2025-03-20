// ✅ WebSocket 서버 연결 (localhost 포트 확인!)
const socket = io("http://localhost:5001", { transports: ["websocket"] });

// ✅ 사용자 닉네임 설정 (세션 저장 -> 브라우저 닫으면 새로 받음)
let userId = sessionStorage.getItem("user_id") || prompt("사용할 닉네임을 입력하세요:", "guest");
if (!userId) userId = "guest" + Math.floor(Math.random() * 1000);
sessionStorage.setItem("user_id", userId);

// ✅ 번역 언어 선택 (localStorage 유지)
let targetLang = localStorage.getItem("target_lang") || "en";
localStorage.setItem("target_lang", targetLang);

// ✅ 사용자 정보 서버에 등록
socket.emit("register", { user_id: userId });
socket.emit("set_language", { user_id: userId, target_lang: targetLang });

console.log(`📢 현재 접속한 사용자 ID: ${userId} (번역 언어: ${targetLang})`);

// ✅ 채팅 박스 및 입력 필드 가져오기
const chatBox = document.getElementById("chat-box");
const messageInput = document.getElementById("message-input");
const targetLangSelect = document.getElementById("target-lang");
const emptyMessage = document.getElementById("empty-chat-message");

// ✅ 번역 언어 변경 시 서버에 전송
targetLangSelect.value = targetLang;
targetLangSelect.addEventListener("change", () => {
    targetLang = targetLangSelect.value;
    localStorage.setItem("target_lang", targetLang);
    socket.emit("set_language", { user_id: userId, target_lang: targetLang });
});

// ✅ 메시지 UI 추가 함수
function addMessage(user_id, original, translated, isOwnMessage) {
    const msgContainer = document.createElement("div");
    msgContainer.classList.add("message");

    if (isOwnMessage) {
        msgContainer.classList.add("user-message");
    } else {
        msgContainer.classList.add("other-message");
    }

    msgContainer.innerHTML = `<strong>${user_id}:</strong> ${original}`;

    if (translated) {
        const translatedElement = document.createElement("div");
        translatedElement.classList.add("translated");
        translatedElement.innerText = `(번역: ${translated})`;
        msgContainer.appendChild(translatedElement);
    }

    chatBox.appendChild(msgContainer);
    chatBox.scrollTop = chatBox.scrollHeight; // 스크롤 자동 이동
}

// ✅ 메시지 전송 함수
function sendMessage() {
    const message = messageInput.value.trim();

    if (message) {
        console.log(`📢 [${userId}] 메시지 전송: ${message}`);

        socket.emit("message", {
            user_id: userId,  // ✅ user_id를 서버로 그대로 전달
            message: message
        });

        messageInput.value = "";
    }
}

// ✅ 엔터 키 입력 시 메시지 전송
messageInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
});

// ✅ 서버에서 메시지를 받을 때
socket.on("message", (data) => {
    console.log("📢 서버에서 메시지 수신:", data);

    const { user_id, original, translated } = data;

    if (emptyMessage) {
        emptyMessage.style.display = "none";
    }

    const isOwnMessage = user_id === userId;
    addMessage(user_id, original, translated, isOwnMessage);
});

// ✅ Socket.IO 연결 이벤트 확인
socket.on("connect", () => {
    console.log("✅ Socket.IO 연결 성공!");
});

// ✅ 오류 발생 시 콘솔에 출력
socket.on("connect_error", (error) => {
    console.error("❌ Socket.IO 연결 오류:", error);
});

