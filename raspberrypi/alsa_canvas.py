import numpy as np
from vispy import gloo
from vispy import app
import alsaaudio as aa
import matplotlib.pyplot as plt
from numpy_ringbuffer import RingBuffer

from pcm_buffer import PCMBuffer


class AlsaCanvas(app.Canvas):
    def __init__(self, device, sample_rate, period, window_size):
        self.sample_rate = sample_rate
        self.window_size = window_size

        self.pcm_buffer = PCMBuffer(
            device=device, sample_rate=sample_rate, period=period, window_size=window_size)

        app.Canvas.__init__(self, title='Use your wheel to zoom!',
                            keys='interactive')

        gloo.set_viewport(0, 0, *self.physical_size)

        gloo.set_state(clear_color='black', blend=True,
                       blend_func=('src_alpha', 'one_minus_src_alpha'))

        self._alsa_sample_timer = app.Timer(
            'auto', connect=self.on_alsa_sample_timer, start=True)

        self.show()

    def on_resize(self, event):
        gloo.set_viewport(0, 0, *event.physical_size)

    def on_draw(self, event):
        pass

    def on_data(self, event):
        pass

    def on_alsa_sample_timer(self, event):
        self.pcm_buffer.read()
        self.on_data(event)
