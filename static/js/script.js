const chatBox = document.getElementById('chatBox');
const userInput = document.getElementById('userInput');
const apiKeyInput = document.getElementById('apiKey');
const modelSelect = document.getElementById('modelSelect');

// 添加消息到聊天框
function addMessage(message, isUser) {
    const div = document.createElement('div');
    div.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    div.textContent = message;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// 发送消息
async function sendMessage() {
    const message = userInput.value.trim();
    const apiKey = apiKeyInput.value.trim();
    const model = modelSelect.value;

    if (!apiKey) return alert('请先输入API密钥');
    if (!message) return;

    addMessage(message, true);
    userInput.value = '';

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                api_key: apiKey,
                model: model
            })
        });

        const data = await response.json();
        if (data.status === 'success') {
            addMessage(data.reply, false);
        } else {
            addMessage(`错误: ${data.reply}`, false);
        }
    } catch (error) {
        addMessage(`请求失败: ${error}`, false);
    }
}

// 回车发送
function handleEnter(e) {
    if (e.key === 'Enter') sendMessage();
}