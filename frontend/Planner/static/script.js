document.addEventListener("DOMContentLoaded", function() {
    const chatBox = document.getElementById("chat-box");
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");

    function appendMessage(content, sender) {
        const messageElement = document.createElement("div");
        
        if (sender === "user") {
            messageElement.classList.add("user-message");
        } else {
            messageElement.classList.add("bot-message");
            content = formatBotMessage(content); // Format chatbot response
        }
    
        messageElement.innerHTML = content; // Use innerHTML to apply formatting
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function formatBotMessage(message) 
    {
        return message
        .replace(/\n/g, "<br>") // Preserve line breaks
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>") // Bold text
        .replace(/\*(.*?)\*/g, "<em>$1</em>") // Italic text
        .replace(/^- (.*?)/gm, "• $1"); // Convert dashes to bullet points
    }   

    sendButton.addEventListener("click", function() {
        const userMessage = messageInput.value.trim();
        if (userMessage === "") return;
        
        appendMessage(userMessage, "user");
        messageInput.value = "";

        fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            appendMessage(data.reply, "bot");
        })
        .catch(error => {
            appendMessage("Error: Unable to connect to the chatbot.", "bot");
        });
    });

    messageInput.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            sendButton.click();
        }
    });
});
