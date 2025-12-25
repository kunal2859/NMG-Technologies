import os
import asyncio
import edge_tts
from faster_whisper import WhisperModel
import tempfile

class STTService:
    """
    Speech-to-Text Service using Faster-Whisper.
    Runs locally to avoid external API latency and costs.
    """
    def __init__(self, model_size="base", device="cpu", compute_type="int8"):
        print(f"INFO: Loading Whisper model ({model_size}) on {device}...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        print("INFO: Whisper model loaded successfully.")

    def transcribe(self, audio_path):
        segments, info = self.model.transcribe(audio_path, beam_size=5)
        text = " ".join([segment.text for segment in segments])
        return text.strip()

class TTSService:
    """
    Text-to-Speech Service using Microsoft Edge's online TTS.
    Provides high-quality neural voices for free.
    """
    def __init__(self, voice="en-US-AriaNeural"):
        self.voice = voice

    async def generate_audio(self, text, output_file):
        print(f"Generating TTS for: {text[:50]}...")
        try:
            communicate = edge_tts.Communicate(text, self.voice)
            await communicate.save(output_file)
            print(f"TTS saved to: {output_file}")
            return output_file
        except Exception as e:
            print(f"TTS Error: {e}")
            raise e