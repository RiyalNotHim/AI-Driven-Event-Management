let bgIndex = 0;
const bgImages = [
    "images/Aesign1.png",
    "images/culture_event.webp",
    "images/tech_event.jpg",
    "images/music_event.jpg"
];

const header = document.querySelector(".header");

function changeBackground() {
    header.style.opacity = 0; // Fade out effect
    setTimeout(() => {
        header.style.backgroundImage = `url('${bgImages[bgIndex]}')`; // Change image
        header.style.opacity = 1; // Fade in effect
        bgIndex = (bgIndex + 1) % bgImages.length; // Loop back after last image
    }, 1000); // Delay before changing
}

// Change background every 4 seconds
setInterval(changeBackground, 4000);


function openSignIn() {
    window.location.href = "login page/main.html";
}
