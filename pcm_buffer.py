import numpy as np
import alsaaudio as aa
from numpy_ringbuffer import RingBuffer


DEVICE = 'hw:Loopback,1'
SAMPLE_RATE = 44100
PERIOD = 1024
CHANNELS = 1
WINDOW_SIZE = SAMPLE_RATE * 2


class PCMBuffer():
    def __init__(self, device=DEVICE, channels=CHANNELS, sample_rate=SAMPLE_RATE, period=PERIOD, window_size=WINDOW_SIZE, dtype=np.float32):
        self.pcm = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NONBLOCK, device=device)
        self.pcm.setchannels(channels)
        self.pcm.setrate(sample_rate)
        self.pcm.setformat(aa.PCM_FORMAT_S32_LE)
        self.pcm.setperiodsize(period)

        self.data_buffer = RingBuffer(capacity=WINDOW_SIZE,
                                      dtype=dtype, allow_overwrite=True)

    def read(self):
        # DO while
        while True:
            length, data = self.pcm.read()
            if length > 0:
                raw = np.frombuffer(data, dtype='<i4')  # LE s32
                self.data_buffer.extend(raw)
            else:
                break

    def data(self):
        return self.data_buffer._unwrap()
