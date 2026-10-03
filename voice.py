"""Hands-free voice: speak replies out loud, listen on the mic, transcribe locally with Whisper.

- Speech-to-text: Hugging Face Whisper on your GPU (English, French and ~100 other languages).
  Audio never leaves the machine.
- Text-to-speech: Microsoft's neural voices via edge-tts (online; the reply text is sent to
  Microsoft's speech service). Falls back to the offline Windows voice if that fails.
- Focus only listens right after it speaks (or when you press Enter in voice mode), never in
  the background, and it doesn't listen while it is talking, so it can't hear itself.
"""
import ctypes
import os
import re
import tempfile
import time
from pathlib import Path

import numpy as np

from . import config

SAMPLE_RATE = 16_000
BLOCK = 480  # 30 ms
# Whisper's classic "hallucinations" on near-silence; ignore them as non-speech.
_PHANTOMS = {"", "you", "thank you.", "thanks for watching!", "merci.", "sous-titres réalisés par la communauté d'amara.org"}


class Voice:
    def __init__(self):
        self.asr = None
        self.threshold = 0.012

    # ---- setup ----------------------------------------------------------

    def load(self):
        """Load Whisper onto the GPU (downloads the model on first use) and measure room noise."""
        import torch
        from transformers import pipeline
        from transformers.utils import logging as hf_logging

        hf_logging.set_verbosity_error()  # keep the chat free of loader warnings and progress bars
        hf_logging.disable_progress_bar()
        cuda = torch.cuda.is_available()
        self.asr = pipeline(
            "automatic-speech-recognition",
            model=config.STT_MODEL,
            dtype=torch.float16 if cuda else torch.float32,
            device="cuda" if cuda else "cpu",
        )
        self.calibrate()

    def calibrate(self, seconds: float = 1.0):
        import sounddevice as sd

        noise = sd.rec(int(seconds * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="float32")
        sd.wait()
        ambient = float(np.sqrt(np.mean(noise ** 2)))
        self.threshold = max(0.008, ambient * 3)

    # ---- listening ------------------------------------------------------

    def listen(self, wait_s: float = 8.0, silence_s: float = 1.2, max_s: float = 45.0) -> str | None:
        """Wait up to wait_s for speech, record until silence_s of quiet, return the transcript."""
        import sounddevice as sd

        frames, started, quiet, t0 = [], False, 0.0, time.monotonic()
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32", blocksize=BLOCK) as stream:
            while True:
                block, _ = stream.read(BLOCK)
                loud = float(np.sqrt(np.mean(block ** 2))) > self.threshold
                if not started:
                    frames = (frames + [block])[-10:]  # keep 300 ms before speech starts
                    if loud:
                        started = True
                    elif time.monotonic() - t0 > wait_s:
                        return None
                    continue
                frames.append(block)
                quiet = 0.0 if loud else quiet + BLOCK / SAMPLE_RATE
                if quiet >= silence_s or len(frames) * BLOCK / SAMPLE_RATE >= max_s:
                    break
        audio = np.concatenate(frames)[:, 0]
        if len(audio) < 0.4 * SAMPLE_RATE:  # a cough or a click, not speech
            return None
        return self.transcribe(audio)

    def transcribe(self, audio: np.ndarray) -> str | None:
        text = self.asr({"raw": audio, "sampling_rate": SAMPLE_RATE},
                        generate_kwargs={"task": "transcribe"})["text"].strip()
        return None if text.lower() in _PHANTOMS else text

    # ---- speaking -------------------------------------------------------

    def speak(self, text: str):
        text = speakable(text)
        if not text:
            return
        try:
            self._speak_edge(text)
        except Exception:  # offline, service change, playback issue: use the built-in voice
            self._speak_sapi(text)

    def _speak_edge(self, text: str):
        import edge_tts

        path = Path(tempfile.gettempdir()) / f"focus_tts_{os.getpid()}.mp3"
        edge_tts.Communicate(text, config.TTS_VOICE, rate=config.TTS_RATE).save_sync(str(path))
        _play_mp3(path)

    def _speak_sapi(self, text: str):
        import win32com.client

        win32com.client.Dispatch("SAPI.SpVoice").Speak(text)


def speakable(text: str) -> str:
    """Strip markdown, emoji and symbols that sound bad when read aloud."""
    text = re.sub(r"`{1,3}[^`]*`{1,3}", "", text)
    text = re.sub(r"[*_#>|]", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)  # [label](url) -> label
    text = re.sub(r"[\U0001F000-\U0001FFFF☀-➿️]", "", text)  # emoji
    text = re.sub(r"^\s*[-•]\s*", "", text, flags=re.M)
    text = re.sub(r"\(\d\)\s*|^\s*\d\.\s+", "", text, flags=re.M)  # (1) / "1." list markers
    return re.sub(r"\s+", " ", text).strip()


def asks_question(text: str) -> bool:
    """Keep the call going only when Focus ended on a question."""
    return speakable(text).rstrip().endswith("?")


def _play_mp3(path: Path):
    """Play an mp3 with the Windows MCI player (built into Windows, no extra dependency)."""
    mci = ctypes.windll.winmm.mciSendStringW
    alias = "focus_tts"
    mci(f"close {alias}", None, 0, 0)
    if mci(f'open "{path}" type mpegvideo alias {alias}', None, 0, 0) != 0:
        raise RuntimeError("could not open audio")
    try:
        mci(f"play {alias} wait", None, 0, 0)
    finally:
        mci(f"close {alias}", None, 0, 0)
