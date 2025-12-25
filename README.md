# ShopAssist - Real-Time Voice AI Agent

Hi! This is my submission for the AI Engineer take-home assignment.
I've built a real-time voice-based AI agent that acts as a customer support representative for an e-commerce store ("ShopAssist").

The goal was to create a system that feels natural to talk to, handles multi-step workflows, and runs entirely on free/open-source models.

## Key Features
*   **Real-Time Voice**: Speak naturally to the agent, and it responds with a generated voice.
*   **Intelligent Agents**:
    *   **Intent Agent**: Understands what you want (Track order, Search, Return, etc.).
    *   **Action Agent**: Executes the logic (using mock data).
    *   **Response Agent**: Crafts a friendly reply.
*   **Context Aware**: It remembers what we talked about (e.g., "Book *it*" works!).
*   **Tech Stack**: Python (FastAPI), WebSockets, Google Gemini (Free Tier), Faster-Whisper, Edge-TTS.

## Technologies Used & Rationale
*   **Python (FastAPI)**: Chosen for its high performance with async capabilities, which is crucial for handling real-time WebSocket connections without blocking. It is also very developer-friendly.
*   **WebSockets**: Essential for real-time, bidirectional audio streaming. HTTP polling would have been too slow for a natural conversation flow.
*   **Google Gemini**: Selected because it offers a generous free tier and low latency, making it ideal for a project requiring fast responses without incurring costs.
*   **Faster-Whisper**: A highly optimized implementation of OpenAI's Whisper model. I chose this over the standard library because it runs significantly faster on CPU, which is important for local deployment.
*   **Edge-TTS**: Provides high-quality, natural-sounding neural voices for free. Most other high-quality TTS options are paid APIs, and standard system TTS sounds too robotic.

## Setup Instructions

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: You may need to install `ffmpeg` on your system if `faster-whisper` or `edge-tts` requires it.*

2.  **Environment Variables**:
    -   Rename `.env.example` to `.env`.
    -   Add your Google Gemini API Key:
        ```
        GEMINI_API_KEY=your_key_here
        ```
    -   Get a free key from [Google AI Studio](https://aistudio.google.com/).

3.  **Run the Server**:
    ```bash
    uvicorn backend.main:app --reload
    ```

4.  **Use the App**:
    -   Open your browser to `http://localhost:8000`.
    -   Click and hold the "Hold to Speak" button.
    -   Ask: "Where is my order #123?" or "Search for gaming mouse".

## Architecture
```text
+--------+       +----------+       +---------+
|  User  | <---> | Frontend | <---> | Backend |
+--------+       +----------+       +----+----+
                                         |
                                         v
                                  +-------------+
                                  | Orchestrator|
                                  +------+------+
                                         |
           +-----------------------------+------------------------------+
           |                             |                              |
           v                             v                              v
    +-------------+               +-------------+                +-------------+
    | STT Service |               | Intent Agent|                | Action Agent|
    +-------------+               +-------------+                +-------------+
           |                             |                              |
           +-----------------------------+------------------------------+
                                         |
                                         v
                                  +-------------+
                                  | Response Agt|
                                  +------+------+
                                         |
                                         v
                                  +-------------+
                                  | TTS Service |
                                  +-------------+
```
-   **Frontend**: Captures audio -> Sends Blob via WebSocket.
-   **Backend**:
    1.  Receives Audio.
    2.  **STT**: Transcribes audio to text.
    3.  **Intent Agent**: Classifies text (Track/Search/Return).
    4.  **Action Agent**: Executes logic (Mock DB).
    5.  **Response Agent**: Generates text response.
    6.  **TTS**: Generates audio from text.
    7.  Returns Audio URL + Text to Frontend.
-   **Frontend**: Plays audio.

## Mock Data
-   **Orders**: 123, 456, 789
-   **Products**: Wireless Headphones, Gaming Mouse, Mechanical Keyboard
