import wave
import numpy as np
import pyaudio
from threading import Thread, Event

class AudioFile(Thread):
    def __init__(self, file, volume=0.5, pitch_shift=1):
        Thread.__init__(self)
        self._pyAudio = pyaudio.PyAudio()
        self._file = wave.open(file, "rb")
        self._chunk_size = self._file.getframerate()
        self._chunk_count = int(self._file.getnframes()/self._chunk_size)
        self._pitch_shift = pitch_shift
        self._volume = volume
        self._audio_stream = self._pyAudio.open(format = self._pyAudio.get_format_from_width(self._file.getsampwidth()),
                channels = self._file.getnchannels(),
                rate = self._file.getframerate(),
                output = True)

    def run(self):
        while True:
            for chunk in range(self._chunk_count):
                da = np.fromstring(self._file.readframes(self._chunk_size), dtype=np.int16)
                left, right = da[0::2], da[1::2]  # left and right channel
                lf, rf = np.fft.rfft(left), np.fft.rfft(right)
                lf, rf = np.roll(lf, self._pitch_shift), np.roll(rf, self._pitch_shift)
                lf[0:self._pitch_shift], rf[0:self._pitch_shift] = 0, 0
                nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
                ns = np.column_stack((nl, nr)).ravel().astype(np.int16)
                self._audio_stream.write(ns.tostring())
            self._file.rewind()

