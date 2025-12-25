// ShopAssist Frontend Logic
// Handles audio recording, WebSocket streaming, and UI updates.

const recordBtn = document.getElementById('record-btn');
const chatLog = document.getElementById('chat-log');
const statusText = document.getElementById('status-text');

let mediaRecorder;
let audioChunks = [];
let ws;
// Generate a random client ID for the session
const clientId = Math.random().toString(36).substring(7);

function connectWebSocket() {
    // Determine protocol (ws or wss) based on current page
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    ws = new WebSocket(`${protocol}//${window.location.host}/ws/${clientId}`);

    ws.onopen = () => {
        console.log("WebSocket connection established.");
        statusText.textContent = "Connected. Ready to speak.";
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleResponse(data);
    };

    ws.onclose = () => {
        console.warn("WebSocket disconnected. Attempting reconnect...");
        statusText.textContent = "Disconnected. Reconnecting...";
        setTimeout(connectWebSocket, 3000);
    };
}

function handleResponse(data) {
    // Add User Message
    addMessage(data.user_text, 'user-msg');

    // Add AI Message
    addMessage(data.ai_text, 'ai-msg');

    // Play Audio
    if (data.audio_url) {
        console.log("Playing audio from:", data.audio_url);
        const audio = new Audio(data.audio_url);
        audio.play().catch(e => {
            console.error("Audio playback error:", e);
            statusText.textContent = "Error playing audio. Check console.";
        });
    }

    statusText.textContent = "Ready";
}

function addMessage(text, className) {
    const div = document.createElement('div');
    div.classList.add('message', className);
    div.textContent = text;
    chatLog.appendChild(div);
    chatLog.scrollTop = chatLog.scrollHeight;
}

// Audio Recording Setup
navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            audioChunks = [];

            if (ws && ws.readyState === WebSocket.OPEN) {
                statusText.textContent = "Processing...";
                ws.send(audioBlob);
            } else {
                statusText.textContent = "Error: WebSocket not connected";
            }
        };
    })
    .catch(err => {
        console.error("Error accessing microphone:", err);
        statusText.textContent = "Error: Microphone access denied";
    });

// Button Events
recordBtn.addEventListener('mousedown', () => {
    if (mediaRecorder && mediaRecorder.state === "inactive") {
        mediaRecorder.start();
        recordBtn.classList.add('recording');
        recordBtn.textContent = "Listening...";
        statusText.textContent = "Recording...";
    }
});

recordBtn.addEventListener('mouseup', () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        recordBtn.classList.remove('recording');
        recordBtn.textContent = "Hold to Speak";
    }
});

// Touch support for mobile
recordBtn.addEventListener('touchstart', (e) => {
    e.preventDefault();
    if (mediaRecorder && mediaRecorder.state === "inactive") {
        mediaRecorder.start();
        recordBtn.classList.add('recording');
        recordBtn.textContent = "Listening...";
        statusText.textContent = "Recording...";
    }
});

recordBtn.addEventListener('touchend', (e) => {
    e.preventDefault();
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        recordBtn.classList.remove('recording');
        recordBtn.textContent = "Hold to Speak";
    }
});

document.getElementById('summary-btn').addEventListener('click', () => {
    fetch(`/summary/${clientId}`)
        .then(res => res.json())
        .then(data => {
            console.log("Session Summary:", data);
            alert("Session Summary logged to console!");
            // Optionally display it in the chat
            addMessage("Session Summary: " + JSON.stringify(data, null, 2), 'ai-msg');
        })
        .catch(err => console.error("Error fetching summary:", err));
});

connectWebSocket();
