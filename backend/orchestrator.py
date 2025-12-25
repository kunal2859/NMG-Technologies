import os
import uuid
from backend.audio_services import STTService, TTSService
from backend.agents import IntentAgent, ActionAgent, ResponseAgent

class Orchestrator:
    """
    Central controller for the voice agent.
    Manages the pipeline: Audio -> STT -> Intent -> Action -> Response -> TTS.
    Also maintains session state and conversation history.
    """
    def __init__(self):
        self.stt = STTService(model_size="base") 
        self.tts = TTSService()
        self.intent_agent = IntentAgent()
        self.action_agent = ActionAgent()
        self.response_agent = ResponseAgent()
        self.sessions = {}
        self.session_data = {}

    async def process_audio(self, session_id, audio_path):
        if session_id not in self.sessions:
            self.sessions[session_id] = []
            self.session_data[session_id] = {
                "session_id": session_id,
                "user_requests": [],
                "operations_performed": [],
                "agent_flow": [],
                "conversation_transcript": []
            }

        # 1. Speech to Text
        print(f"Transcribing audio for session {session_id}...")
        user_text = self.stt.transcribe(audio_path)
        print(f"User said: {user_text}")
        
        if not user_text:
            return None, "I didn't hear anything."

        self.sessions[session_id].append({"role": "user", "content": user_text})
        self.session_data[session_id]["conversation_transcript"].append(f"User: {user_text}")
        self.session_data[session_id]["user_requests"].append(user_text)

        # 2. Intent Classification
        print("Analyzing intent...")
        intent_data = await self.intent_agent.analyze(user_text, history=self.sessions[session_id])
        print(f"Intent: {intent_data}")
        
        self.session_data[session_id]["agent_flow"].append("IntentAgent")

        # 3. Action Execution
        print("Executing action...")
        action_result = self.action_agent.execute(intent_data)
        print(f"Action Result: {action_result}")
        
        self.session_data[session_id]["agent_flow"].append("ActionAgent")
        self.session_data[session_id]["operations_performed"].append(intent_data.get("intent"))

        # 4. Response Generation
        print("Generating response...")
        response_text = await self.response_agent.generate_response(user_text, action_result)
        print(f"AI Response: {response_text}")
        
        self.session_data[session_id]["agent_flow"].append("ResponseAgent")

        self.sessions[session_id].append({"role": "ai", "content": response_text})
        self.session_data[session_id]["conversation_transcript"].append(f"AI: {response_text}")

        # 5. Text to Speech
        print("Generating audio response...")
        output_filename = f"response_{uuid.uuid4().hex}.mp3"
        output_path = os.path.join("frontend", "public", "audio", output_filename)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        await self.tts.generate_audio(response_text, output_path)

        return {
            "user_text": user_text,
            "ai_text": response_text,
            "audio_url": f"/audio/{output_filename}",
            "intent": intent_data.get("intent"),
            "action_result": action_result
        }

    def get_session_summary(self, session_id):
        return self.session_data.get(session_id, {})
