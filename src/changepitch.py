import wave
import numpy as np
import pyaudio
import threading
import audiofile

shift = 500

audioThread = audiofile.AudioFile(file = "./assets/test.wav", pitch_shift = shift)
audioThread.run()