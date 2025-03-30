document.addEventListener("DOMContentLoaded", () => {
    function scheduleUserNotification() {
        const message = document.getElementById("message").value.trim();
        const dateInput = document.getElementById("date").value;
        const timeInput = document.getElementById("time").value;
        const repeatOption = document.getElementById("repeat").value;
        const confirmationMessage = document.getElementById("confirmationMessage");

        if (!message) {
            alert("Please enter a notification message.");
            return;
        }

        if (!dateInput || !timeInput) {
            alert("Please select a valid date and time.");
            return;
        }

        const selectedDate = new Date(dateInput + "T" + timeInput);
        const now = new Date();

        if (selectedDate < now) {
            alert("Please select a future date and time.");
            return;
        }

        const timeUntilNotification = selectedDate - now;

        console.log(`Notification scheduled in ${timeUntilNotification / 1000} seconds`);

        // Show confirmation message ✅
        confirmationMessage.classList.remove("hidden");

        setTimeout(() => {
            sendNotification(message);
            if (repeatOption === "daily") {
                startDailyNotifications(selectedDate.getHours(), selectedDate.getMinutes(), message);
            }
        }, timeUntilNotification);
    }

    function startDailyNotifications(hour, minute, message) {
        setInterval(() => {
            const now = new Date();
            if (now.getHours() === hour && now.getMinutes() === minute) {
                sendNotification(message);
            }
        }, 60000); // Check every minute
    }

    function sendNotification(message) {
        Notification.requestPermission().then(permission => {
            if (permission === "granted") {
                new Notification("Reminder ⏰", {
                    body: message,
                    requireInteraction: true,
                });
                console.log("Notification sent!");
            } else {
                console.log("Notifications are blocked!");
            }
        });
    }

    window.scheduleUserNotification = scheduleUserNotification;
});
