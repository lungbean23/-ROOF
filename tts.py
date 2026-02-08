"""
Text-to-Speech module for ┴ROOF Radio
Using Edge-TTS for free, high-quality voices
"""

import subprocess
import platform
import os
import asyncio
import tempfile
from pathlib import Path

# Try to import edge_tts
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

class TTS:
    def __init__(self, voice_type="edge"):
        self.voice_type = voice_type if EDGE_TTS_AVAILABLE else "text"
        self.system = platform.system()
        self.temp_dir = Path(tempfile.gettempdir()) / "troof_audio"
        self.temp_dir.mkdir(exist_ok=True)
        
        if not EDGE_TTS_AVAILABLE and voice_type == "edge":
            print("[Note: edge-tts not installed. Using text output only.]")
            print("[Install with: pip install edge-tts]")
    
    def speak(self, text, speaker_name):
        """
        Convert text to speech and play it
        Falls back to text output if TTS is unavailable
        """
        
        # Always print the text
        border = "─" * 80
        print(f"\n{border}")
        print(f"🎙️  {speaker_name}")
        print(f"{border}")
        print(f"{text}")
        print(f"{border}\n")
        
        # If edge-tts is available, also speak it
        if self.voice_type == "edge" and EDGE_TTS_AVAILABLE:
            try:
                asyncio.run(self._speak_edge_tts_async(text, speaker_name))
            except Exception as e:
                print(f"[Audio playback failed: {e}]")
    
    async def _speak_edge_tts_async(self, text, speaker_name):
        """Use Edge TTS (async version for proper implementation)"""
        # Get voice for this speaker
        voice = VOICE_MAP.get(speaker_name, {}).get("edge", "en-US-GuyNeural")
        
        # Generate audio file
        audio_file = self.temp_dir / f"{speaker_name}_{int(asyncio.get_event_loop().time())}.mp3"
        
        # Create TTS
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(str(audio_file))
        
        # Play the audio
        self._play_audio(audio_file)
        
        # Clean up
        try:
            audio_file.unlink()
        except:
            pass
    
    def _play_audio(self, audio_file):
        """Play an audio file"""
        try:
            if self.system == "Linux":
                # Try different Linux audio players
                for player in ['mpg123', 'ffplay', 'cvlc', 'mpv']:
                    try:
                        subprocess.run([player, str(audio_file)], 
                                     check=True, 
                                     stdout=subprocess.DEVNULL, 
                                     stderr=subprocess.DEVNULL)
                        return
                    except (FileNotFoundError, subprocess.CalledProcessError):
                        continue
                print("[No audio player found. Install mpg123 or mpv]")
                
            elif self.system == "Darwin":  # macOS
                subprocess.run(['afplay', str(audio_file)], check=True)
                
            elif self.system == "Windows":
                os.startfile(audio_file)
        except Exception as e:
            print(f"[Audio playback error: {e}]")


# Voice assignments for each host
VOICE_MAP = {
    "Goku": {
        "edge": "en-US-GuyNeural",  # Energetic, clear voice
        "espeak": "en+m3",
        "piper": "en_US-lessac-medium"
    },
    "Homer": {
        "edge": "en-US-ChristopherNeural",  # More relaxed, conversational
        "espeak": "en+m7",
        "piper": "en_US-ryan-medium"
    }
}


def get_tts_engine(voice_type="edge"):
    """Factory function to get TTS engine"""
    return TTS(voice_type=voice_type)
