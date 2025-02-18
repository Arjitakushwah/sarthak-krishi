// Chatbot toggle function
function toggleChat() {
    const chatbox = document.getElementById('chatbox');
    chatbox.style.display = chatbox.style.display === 'none' ? 'flex' : 'none';
}

// Function to handle message sending
async function sendMessage() {
    const inputField = document.getElementById('userMessage');
    const message = inputField.value.trim();
    if (message) {
        const chatboxBody = document.getElementById('chatbox-body');
        const userMessage = document.createElement('div');
        userMessage.textContent = `You: ${message}`;
        chatboxBody.appendChild(userMessage);

        // Clear input
        inputField.value = '';

        // Simulate chatbot reply (fetch response from API)
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        if (data.error) {
            const errorMessage = document.createElement('div');
            errorMessage.textContent = `Error: ${data.error}`;
            chatboxBody.appendChild(errorMessage);
        } else {
            const botMessage = document.createElement('div');
            botMessage.textContent = `Bot: ${data.response}`;
            chatboxBody.appendChild(botMessage);
        }

        // Scroll to the bottom
        chatboxBody.scrollTop = chatboxBody.scrollHeight;
    }
}
