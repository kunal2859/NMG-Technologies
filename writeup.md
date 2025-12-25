# Brief Write-up: Real-Time Voice AI Agent

## How I Designed the Agent Collaboration
I decided to build this system using a modular multi-agent architecture because it allows for better separation of concerns. I used a central `Orchestrator` to manage the flow, which I found to be the most reliable pattern for this kind of linear pipeline.

Here's how I structured the workflow:

1.  **Input Processing**: I used `faster-whisper` for STT because it's significantly faster than the standard Whisper library and runs well on CPU.
2.  **Intent Agent**: This is the "brain". I used Google Gemini to analyze the text. I specifically added a `history` parameter to the analysis function so it could understand context (like "book *it*").
3.  **Action Agent**: I kept this separate to mimic a real microservice. It handles the business logic (mock database lookups).
4.  **Response Agent**: I wanted the voice responses to sound natural, so I created a dedicated agent just to format the text for TTS, ensuring it's concise.
5.  **Output**: For TTS, I chose `edge-tts` because it offers high-quality neural voices for free, which was a key requirement.

### Architecture Diagram
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

## Challenges & Solutions
**1. Context Awareness**: Initially, the system treated every query in isolation. This made flows like "Do you have mice?" -> "Book it" impossible because the second query lacked product information.
*   **Solution**: I updated the `Orchestrator` to maintain a session-based conversation history and passed this history to the `IntentAgent`. This allowed the LLM to resolve references from previous turns effectively.

**2. Model Availability**: During development, the `gemini-1.5-flash` model returned 404 errors due to versioning or deprecation issues in the library.
*   **Solution**: I wrote a script to list available models and switched to the stable `gemini-pro` (or `gemini-2.5-flash` if available) to ensure reliability.

**3. Audio Latency**: Real-time voice requires low latency. Generating audio files and serving them via static URLs introduced a slight delay.
*   **Solution**: I optimized the pipeline by using `edge-tts` (which is faster than many local models) and ensured asynchronous processing in FastAPI to handle concurrent requests without blocking.

## Future Improvements
With more time, I would focus on the following:
1.  **Interruption Handling**: Currently, the system processes one turn at a time. Implementing "barge-in" capability would allow users to interrupt the AI while it's speaking, making the conversation feel much more natural.
2.  **RAG Integration**: Instead of hardcoded mock data, I would integrate a Vector Database (RAG) to allow the agent to search through a real product catalog or knowledge base documentation.
3.  **Latency Optimization**: I would implement audio streaming (chunked transfer) instead of generating the full MP3 file before playing. This would significantly reduce the "time-to-first-byte" for the audio response.
