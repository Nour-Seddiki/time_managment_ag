"""Hands-free voice: speak replies out loud, listen on the mic, transcribe locally with Whisper.

- Speech-to-text: Hugging Face Whisper on your GPU (English, French and ~100 other languages).
  Audio never leaves the machine.
- Turn-taking: Silero VAD (a small neural speech detector) decides when you start and stop
  talking, so background noise doesn't open or hold the mic. Falls back to a loudness threshold.
- Text-to-speech: Microsoft's neural voices via edge-tts (online; the reply text is sent to
  Microsoft's speech service), synthesized sentence by sentence so Focus starts talking after the
  first one. Falls back to the offline Windows voice. Press Enter to cut Focus off mid-sentence.
- Focus only listens right after it speaks (a short tone marks your turn) or when you press
  Enter, never in the background, and never while it is talking, so it can't hear itself.
"""
import ctypes
import os
import queue
import re
import tempfile
import threading
import time
import uuid
from pathlib import Path

import numpy as np

from . import config

SAMPLE_RATE = 16_000
BLOCK = 512  # 32 ms; the chunk size Silero VAD expects at 16 kHz
# Whisper's classic "hallucinations" on near-silence; ignore them as non-speech.
_PHANTOMS = {"", "you", "thank you.", "thanks for watching!", "merci.", "sous-titres réalisés par la communauté d'amara.org"}


class Endpointer:
    """Turns a stream of 32 ms chunks into one utterance: wait for speech, stop after trailing silence.

    Uses hysteresis on the speech probability (start above start_th, count as silence below end_th)
    and keeps a short pre-roll so the first syllable isn't clipped.
    """

    def __init__(self, speech_prob, silence_s=1.0, start_th=0.5, end_th=0.35, preroll=8):
        self.speech_prob, self.silence_s = speech_prob, silence_s
        self.start_th, self.end_th, self.preroll = start_th, end_th, preroll
        self.chunks, self.state, self.quiet_s, self.speech_s = [], "waiting", 0.0, 0.0

    def feed(self, chunk: np.ndarray) -> str:
        p = self.speech_prob(chunk)
        dt = len(chunk) / SAMPLE_RATE
        if self.state == "waiting":
            self.chunks = (self.chunks + [chunk])[-self.preroll:]
            if p >= self.start_th:
                self.state = "speaking"
                self.speech_s = dt
            return self.state
        self.chunks.append(chunk)
        if p < self.end_th:
            self.quiet_s += dt
        else:
            self.quiet_s, self.speech_s = 0.0, self.speech_s + dt
        if self.quiet_s >= self.silence_s:
            self.state = "done"
        return self.state

    @property
    def duration_s(self) -> float:
        return sum(len(c) for c in self.chunks) / SAMPLE_RATE

    @property
    def audio(self) -> np.ndarray:
        return np.concatenate(self.chunks) if self.chunks else np.zeros(0, dtype=np.float32)


class Voice:
    def __init__(self):
        self.asr = None
        self.vad = None
        self.threshold = 0.012  # loudness fallback when Silero isn't available
        self.speaking = False
        self.interrupt = threading.Event()
        self.interrupt_reason = None  # "enter" (talk now) or "text" (a typed message is coming)

    # ---- setup ----------------------------------------------------------

    def load(self):
        """Load Whisper onto the GPU and the speech detector, and measure room noise."""
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
        try:
            from silero_vad import load_silero_vad

            self.vad = load_silero_vad()
        except Exception:  # not installed: use the loudness threshold instead
            self.vad = None
        threading.Thread(target=self.warm_up_tts, daemon=True, name="tts-warmup").start()
        self.calibrate()

    def warm_up_tts(self):
        """The first edge-tts request in a process takes seconds (TLS, imports); pay it before the first reply."""
        try:
            import edge_tts

            path = Path(tempfile.gettempdir()) / f"focus_tts_warm_{os.getpid()}.mp3"
            edge_tts.Communicate("Hi.", config.TTS_VOICE, rate=config.TTS_RATE).save_sync(str(path))
            path.unlink(missing_ok=True)
        except Exception:
            pass

    def calibrate(self, seconds: float = 1.0):
        import sounddevice as sd

        noise = sd.rec(int(seconds * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="float32")
        sd.wait()
        ambient = float(np.sqrt(np.mean(noise ** 2)))
        self.threshold = max(0.008, ambient * 3)

    def speech_prob(self, chunk: np.ndarray) -> float:
        if self.vad is None:
            return 1.0 if float(np.sqrt(np.mean(chunk ** 2))) > self.threshold else 0.0
        import torch

        with torch.no_grad():
            return float(self.vad(torch.from_numpy(np.ascontiguousarray(chunk, dtype=np.float32)), SAMPLE_RATE).item())

    # ---- listening ------------------------------------------------------

    def listen(self, wait_s: float = 8.0, silence_s: float = 1.0, max_s: float = 45.0, on_speech=None) -> str | None:
        """Play the your-turn tone, wait up to wait_s for speech, record until silence, transcribe."""
        import sounddevice as sd

        your_turn_tone()
        if self.vad is not None:
            self.vad.reset_states()
        ep, t0 = Endpointer(self.speech_prob, silence_s), time.monotonic()
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32", blocksize=BLOCK) as stream:
            while True:
                block, _ = stream.read(BLOCK)
                before = ep.state
                state = ep.feed(block[:, 0])
                if before == "waiting" and state == "speaking" and on_speech:
                    on_speech()
                if state == "waiting" and time.monotonic() - t0 > wait_s:
                    return None
                if state == "done" or ep.duration_s >= max_s:
                    break
        if ep.speech_s < 0.3:  # a cough or a click, not speech
            return None
        return self.transcribe(ep.audio)

    def transcribe(self, audio: np.ndarray) -> str | None:
        text = self.asr({"raw": audio, "sampling_rate": SAMPLE_RATE},
                        generate_kwargs={"task": "transcribe"})["text"].strip()
        return None if text.lower() in _PHANTOMS else text

    # ---- speaking -------------------------------------------------------

    def speak(self, text: str) -> bool:
        """Read text aloud, sentence by sentence. Returns True if it was interrupted."""
        self.interrupt.clear()
        self.interrupt_reason = None
        sentences = split_sentences(speakable(text))
        if not sentences:
            return False
        self.speaking = True
        try:
            return self._speak_edge(sentences)
        finally:
            self.speaking = False

    def stop(self, reason: str = "enter"):
        """Cut Focus off (called from the keyboard thread)."""
        self.interrupt_reason = reason
        self.interrupt.set()

    def _speak_edge(self, sentences: list[str]) -> bool:
        """Synthesize the next sentence while the current one plays."""
        import edge_tts

        out: queue.Queue = queue.Queue()
        tmp = Path(tempfile.gettempdir())

        def produce():
            for i, sentence in enumerate(sentences):
                if self.interrupt.is_set():
                    break
                path = tmp / f"focus_tts_{os.getpid()}_{uuid.uuid4().hex[:6]}.mp3"
                try:
                    edge_tts.Communicate(sentence, config.TTS_VOICE, rate=config.TTS_RATE).save_sync(str(path))
                except Exception:  # offline or service change: hand the rest to the Windows voice
                    out.put((i, None))
                    return
                out.put((i, path))
            out.put((len(sentences), None))

        threading.Thread(target=produce, daemon=True, name="tts").start()
        while True:
            i, path = out.get()
            if path is None:
                return self._speak_sapi(sentences[i:]) if i < len(sentences) else False
            try:
                if _play_mp3(path, self.interrupt):
                    return True
            except Exception:  # playback failed: say this sentence and the rest offline
                return self._speak_sapi(sentences[i:])
            finally:
                path.unlink(missing_ok=True)

    def _speak_sapi(self, sentences: list[str]) -> bool:
        import pythoncom
        import win32com.client

        pythoncom.CoInitialize()  # speech runs in a worker thread
        try:
            voice = win32com.client.Dispatch("SAPI.SpVoice")
            for sentence in sentences:
                voice.Speak(sentence, 1)  # SVSFlagsAsync
                while not voice.WaitUntilDone(50):
                    if self.interrupt.is_set():
                        voice.Speak("", 3)  # purge: stop talking now
                        return True
            return False
        finally:
            pythoncom.CoUninitialize()


def speakable(text: str) -> str:
    """Strip markdown, emoji and symbols that sound bad when read aloud."""
    text = re.sub(r"`{1,3}[^`]*`{1,3}", "", text)
    text = re.sub(r"[*_#>|]", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)  # [label](url) -> label
    text = re.sub(r"[\U0001F000-\U0001FFFF☀-➿️]", "", text)  # emoji
    text = re.sub(r"^\s*[-•]\s*", "", text, flags=re.M)
    text = re.sub(r"\(\d\)\s*|^\s*\d\.\s+", "", text, flags=re.M)  # (1) / "1." list markers
    return re.sub(r"\s+", " ", text).strip()


def split_sentences(text: str, min_chars: int = 25) -> list[str]:
    """Sentence chunks for incremental speech; tiny fragments ("Nice!") ride along with the next."""
    parts = [p for p in re.split(r"(?<=[.!?…])\s+", text) if p]
    chunks: list[str] = []
    for part in parts:
        if chunks and len(chunks[-1]) < min_chars:
            chunks[-1] = f"{chunks[-1]} {part}"
        else:
            chunks.append(part)
    return chunks


def asks_question(text: str) -> bool:
    """Keep the call going only when Focus ended on a question."""
    return speakable(text).rstrip().endswith("?")


def your_turn_tone():
    """Short rising two-note tone: the mic is open."""
    try:
        import winsound

        winsound.Beep(660, 70)
        winsound.Beep(880, 90)
    except Exception:
        pass


def _play_mp3(path: Path, stop: threading.Event | None = None) -> bool:
    """Play an mp3 with the Windows MCI player (built into Windows). Returns True if stopped early."""
    mci = ctypes.windll.winmm.mciSendStringW
    alias = f"focus_tts_{uuid.uuid4().hex[:8]}"
    if mci(f'open "{path}" type mpegvideo alias {alias}', None, 0, 0) != 0:
        raise RuntimeError("could not open audio")
    try:
        if mci(f"play {alias}", None, 0, 0) != 0:
            raise RuntimeError("could not play audio")
        mode = ctypes.create_unicode_buffer(32)
        deadline = time.monotonic() + 120
        while time.monotonic() < deadline:
            if stop is not None and stop.is_set():
                mci(f"stop {alias}", None, 0, 0)
                return True
            mci(f"status {alias} mode", mode, 32, 0)
            if mode.value == "stopped":
                return False
            time.sleep(0.03)
        return False
    finally:
        mci(f"close {alias}", None, 0, 0)
