import os
import re
import uuid
from backend.audio_services import STTService, TTSService
from backend.langchain_agent import LangChainAgent
from backend.logger import setup_logger

logger = setup_logger(__name__)

class Orchestrator:
    def __init__(self):
        self.stt = STTService(model_size="base") 
        self.tts = TTSService()
        self.agent = LangChainAgent()
        self.sessions = {}
        self.session_data = {}

    async def process_audio(self, session_id, audio_path):
        if session_id not in self.sessions:
            self.sessions[session_id] = []
            self.session_data[session_id] = {
                "session_id": session_id,
                "user_requests": [],
                "agent_responses": [],
                "conversation_transcript": []
            }

        logger.info(f"Transcribing audio for session {session_id}...")
        user_text = self.stt.transcribe(audio_path)
        logger.info(f"User said: {user_text}")
        
        if not user_text:
            return None, "I didn't hear anything."

        self.sessions[session_id].append({"role": "user", "content": user_text})
        self.session_data[session_id]["conversation_transcript"].append(f"User: {user_text}")
        self.session_data[session_id]["user_requests"].append(user_text)

        logger.info("Invoking LangChain Agent...")
        response_text = await self.agent.process_message(user_text, self.sessions[session_id])
        logger.info(f"AI Response: {response_text}")
        
        self.sessions[session_id].append({"role": "ai", "content": response_text})
        self.session_data[session_id]["conversation_transcript"].append(f"AI: {response_text}")
        self.session_data[session_id]["agent_responses"].append(response_text)

        logger.info("Generating audio response...")
        
        tts_text = re.sub(r'\*\*([^*]+)\*\*', r'\1', response_text)  
        tts_text = re.sub(r'\*([^*]+)\*', r'\1', tts_text) 
        tts_text = re.sub(r'#+\s*', '', tts_text) 
        tts_text = re.sub(r'-\s+', '', tts_text) 
        
        output_filename = f"response_{uuid.uuid4().hex}.mp3"
        output_path = os.path.join("frontend", "public", "audio", output_filename)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        await self.tts.generate_audio(tts_text, output_path)

        return {
            "user_text": user_text,
            "ai_text": response_text,
            "audio_url": f"/audio/{output_filename}",
            "intent": "processed_by_agent", 
            "action_result": {} 
        }

    def get_session_summary(self, session_id):
        return self.session_data.get(session_id, {})
