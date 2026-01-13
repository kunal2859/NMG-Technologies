import os
import asyncio
import edge_tts
from faster_whisper import WhisperModel
import tempfile
from backend.logger import setup_logger

logger = setup_logger(__name__)

class STTService:
    def __init__(self, model_size="base", device="cpu", compute_type="int8"):
        logger.info(f"Loading Whisper model ({model_size}) on {device}...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        logger.info("Whisper model loaded successfully")

    def transcribe(self, audio_path):
        segments, info = self.model.transcribe(audio_path, beam_size=5)
        text = " ".join([segment.text for segment in segments])
        return text.strip()

class TTSService:
    def __init__(self, voice="en-US-AriaNeural"):
        self.voice = voice

    async def generate_audio(self, text, output_file):
        logger.debug(f"Generating TTS for: {text[:50]}...")
        try:
            communicate = edge_tts.Communicate(text, self.voice)
            await communicate.save(output_file)
            logger.debug(f"TTS saved to: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"TTS Error: {e}", exc_info=True)
            raise e