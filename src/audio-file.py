import wave
import numpy as np
import pyaudio
from threading import Thread, Event

class AudioFile(Thread):
    def __init__(self, file, volume=0.5, pitch_shift=1):
        Thread.__init__(self)
        self._stop = Event()
        self._file = wave.open(file, "rb")
        self._chunk_size = self._file.getframerate()
        self._chunk_count = int(self._file.getnframes()/self._chunk_size)
        self._pitch_shift = pitch_shift
        self._volume = volume
        self._audio_stream = pyaudio.PyAudio().open(format = pyAudio.get_format_from_width(readFile.getsampwidth()),
                channels = self._file.getnchannels(),
                rate = self._file.getframerate(),
                output = True)

    def run(self):
        

