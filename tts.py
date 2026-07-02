import asyncio
import numpy as np
import pyaudio
from kokoro import KPipeline

SAMPLE_RATE = 24000
VOICE = "pf_dora"  # voz feminina em pt-br

_pipeline: KPipeline | None = None

def _get_pipeline() -> KPipeline:
    global _pipeline
    if _pipeline is None:
        _pipeline = KPipeline(lang_code="p", repo_id="hexgrad/Kokoro-82M")
    return _pipeline

def _synthesize_and_play(text: str) -> None:
    pipeline = _get_pipeline()
    player = pyaudio.PyAudio()
    stream = player.open(format=pyaudio.paFloat32, channels=1, rate=SAMPLE_RATE, output=True)

    try:
        for result in pipeline(text, voice=VOICE):
            if result.audio is None:
                continue
            audio = result.audio.numpy().astype(np.float32)
            stream.write(audio.tobytes())
    finally:
        stream.stop_stream()
        stream.close()
        player.terminate()

async def speak(text: str) -> None:
    if not text.strip():
        return
    await asyncio.to_thread(_synthesize_and_play, text)
