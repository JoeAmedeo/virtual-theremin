import wave
import numpy as np
import pyaudio
import threading

pyAudio = pyaudio.PyAudio()
readFile = wave.open("./assets/test.wav", "rb")
stream = pyAudio.open(format = pyAudio.get_format_from_width(readFile.getsampwidth()),
                      channels = readFile.getnchannels(),
                      rate = readFile.getframerate(),
                      output = True)


size = readFile.getframerate()  # Read and process 1/fr second at a time.
# A larger number for fr means less reverb.
count = int(readFile.getnframes()/size)  # count of the whole file
shift = 500


def play_sound():
    while True:
        for num in range(count):
            da = np.fromstring(readFile.readframes(size), dtype=np.int16)
            left, right = da[0::2], da[1::2]  # left and right channel
            lf, rf = np.fft.rfft(left), np.fft.rfft(right)
            lf, rf = np.roll(lf, shift), np.roll(rf, shift)
            lf[0:shift], rf[0:shift] = 0, 0
            nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
            ns = np.column_stack((nl, nr)).ravel().astype(np.int16)
            stream.write(ns.tostring())
        readFile.rewind()

audioStreamThread = threading.Thread(target=play_sound)
audioStreamThread.start()


readFile.close()
stream.close()