
// File upload functionality
const uploadContainer = document.getElementById('uploadContainer');
const fileInput = document.getElementById('fileInput');
const mediaPreview = document.getElementById('mediaPreview');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');

if (uploadContainer && fileInput) {
    // Clicking the container opens file dialog
    uploadContainer.addEventListener('click', () => {
        fileInput.click();
    });

    // When a file is selected
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];

            // Show file name
            fileName.textContent = file.name;

            // Show formatted file size
            const size = file.size;
            const i = Math.floor(Math.log(size) / Math.log(1024));
            const formattedSize = (size / Math.pow(1024, i)).toFixed(2) + ' ' + ['B', 'kB', 'MB', 'GB', 'TB'][i];
            fileSize.textContent = formattedSize;

            // Show preview if image or video
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    mediaPreview.src = e.target.result;
                    mediaPreview.style.display = 'block';
                }
                reader.readAsDataURL(file);
       } else if (file.type.startsWith('video/')) {
    const reader = new FileReader();
    reader.onload = function(e) {
        mediaPreview.src = e.target.result;
        mediaPreview.style.display = 'block';
        mediaPreview.load();
    }
    reader.readAsDataURL(file);
} else {
    mediaPreview.style.display = 'none';
}
            // Show file info container
            fileInfo.style.display = 'block';
        }
    });
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;

        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});
// ================= Chatbot =================
const chatForm = document.getElementById("chatForm");
const chatMessage = document.getElementById("chatMessage");
const chatWindow = document.getElementById("chatWindow");

if (chatForm) {
    chatForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const message = chatMessage.value.trim();
        if (!message) return;

        // Display user message
        chatWindow.innerHTML += `<div class="message user"><strong>You:</strong> ${message}</div>`;
        chatMessage.value = "";

        // Auto scroll
        chatWindow.scrollTop = chatWindow.scrollHeight;

        // Send to server
        const response = await fetch("/chatbot", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: `message=${encodeURIComponent(message)}`
        });

        const data = await response.json();
        chatWindow.innerHTML += `<div class="message bot"><strong>TruthNet AI:</strong> ${data.response}</div>`;
        chatWindow.scrollTop = chatWindow.scrollHeight;
    });
}
