let socket;

function connectWebSocket() {
    const email = document.getElementById("email").value;
    if (!email) {
        alert("Enter your email first!");
        return;
    }

    socket = new WebSocket(`ws://localhost:8000/ws/${encodeURIComponent(email)}`);

    socket.onopen = function () {
        console.log("✅ WebSocket connected!");
        document.getElementById("status").innerText = "Connected!";
    };

    socket.onerror = function (error) {
        console.error("❌ WebSocket error:", error);
    };

    socket.onmessage = function (event) {
        console.log("🔔 Notification received:", event.data);
        const notificationDiv = document.getElementById("notifications");
        const message = document.createElement("p");
        message.innerText = `📢 ${event.data}`;
        notificationDiv.appendChild(message);
    };

    socket.onclose = function () {
        console.log("⚠️ WebSocket closed!");
        document.getElementById("status").innerText = "Disconnected!";
    };
}
