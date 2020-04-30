import wave
import numpy as np
import pyaudio

chunk = 1024
pyAudio = pyaudio.PyAudio()
readFile = wave.open("./assets/test.wav", "rb")
writeFile = wave.open("./assets/temp.wav", "wb")

# Set the parameters for the output file.
parameters = list(readFile.getparams())
parameters[3] = 0  # The number of samples will be set by writeframes.
parameters = tuple(parameters)
writeFile.setparams(parameters)
fr = 20
size = readFile.getframerate()//fr  # Read and process 1/fr second at a time.
# A larger number for fr means less reverb.
count = int(readFile.getnframes()/size)  # count of the whole file
shift = 100//fr  # shifting 100 Hz
for num in range(count):
    da = np.fromstring(readFile.readframes(size), dtype=np.int16)
    left, right = da[0::2], da[1::2]  # left and right channel
    lf, rf = np.fft.rfft(left), np.fft.rfft(right)
    lf, rf = np.roll(lf, shift), np.roll(rf, shift)
    lf[0:shift], rf[0:shift] = 0, 0
    nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
    ns = np.column_stack((nl, nr)).ravel().astype(np.int16)
    writeFile.writeframes(ns.tostring())

stream = pyAudio.open(format = pyAudio.get_format_from_width(readFile.getsampwidth()),
                      channels = readFile.getnchannels(),
                      rate = readFile.getframerate(),
                      output = True)
writeFile.close()
idkWhatImDoing = wave.open("./assets/temp.wav", "rb")
data = idkWhatImDoing.readframes(chunk)


while data:
    stream.write(data)
    data = idkWhatImDoing.readframes(chunk)


readFile.close()
idkWhatImDoing.close()