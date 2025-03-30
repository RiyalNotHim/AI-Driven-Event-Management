document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("surveyForm").addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent default form submission
        
        const formData = {
            name: document.getElementById("name").value,
            email: document.getElementById("email").value,
            mobile: document.getElementById("mobile").value,
            experience: document.getElementById("experience").value
        };

        try {
            const response = await fetch("http://localhost:5000/submit", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                alert("✅ Form submitted successfully!");
                window.location.href = "thanky.html"; // Redirect on success
            } else {
                alert("❌ Failed to submit form!");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("❌ Something went wrong!");
        }
    });
});
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("surveyForm").addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent actual form submission
        window.location.href = "thanky.html"; // Redirect to thank-you page
    });
});
