const container   = document.querySelector('.container')
const registerBtn   = document.querySelector('.register-btn')
const loginBtn   = document.querySelector('.login-btn')

registerBtn.addEventListener('click' , () =>{
    container.classList.add('active')
});

loginBtn.addEventListener('click' , () => {
    container.classList.remove('active')
});


document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.querySelector(".registration form"); // ✅ Selects the registration form
    const loginForm = document.querySelector(".login form"); // ✅ Selects the login form

    // ✅ Handle Registration
    if (registerForm) {
        registerForm.addEventListener("submit", async function (e) {
            e.preventDefault();

            const username = document.getElementById("username")?.value.trim();
            const email = document.getElementById("email")?.value.trim();
            const password = document.getElementById("password")?.value.trim();

            if (!username || !email || !password) {
                alert("❌ All fields are required!");
                return;
            }

            try {
                const response = await fetch("http://localhost:5000/register", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, email, password })
                });

                const data = await response.json();

                if (response.ok) {
                    alert("✅ Registration Successful!");
                    window.location.href = "home.html";  // Redirect after successful registration
                } else {
                    alert(`❌ Error: ${data.message}`);
                }
            } catch (error) {
                console.error("❌ Fetch error:", error);
                alert("❌ Server is not responding.");
            }
        });
    } else {
        console.error("❌ Registration form not found!");
    }

    // ✅ Handle Login
    if (loginForm) {
        loginForm.addEventListener("submit", async function (e) {
            e.preventDefault();

            const email = document.getElementById("login-email")?.value.trim();
            const password = document.getElementById("login-password")?.value.trim();

            if (!email || !password) {
                alert("❌ Email and Password are required!");
                return;
            }

            try {
                const response = await fetch("http://localhost:5000/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();
                alert(data.message);

                if (data.redirect) {
                    window.location.href = data.redirect; // ✅ Redirects to dashboard/home.html
                }
            } catch (error) {
                console.error("❌ Fetch error:", error);
                alert("❌ Server is not responding.");
            }
        });
    } else {
        console.error("❌ Login form not found!");
    }
});
