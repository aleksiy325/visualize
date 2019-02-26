import math
import numpy as np
from vispy import gloo
from vispy import app
from librosa import beat

from alsa_canvas import AlsaCanvas


DEVICE = 'hw:Loopback,1'
SAMPLE_RATE = 44100
PERIOD = 1024
WINDOW_SIZE = PERIOD * 1

AUDIO_SIGNAL_VERT_SHADER = """
attribute vec2 point_data;
varying vec4 f_color;
uniform vec2 u_scale;

void main () {
    gl_Position = vec4(point_data.x * u_scale.x,
                       point_data.y * u_scale.y, 0, 1);
    f_color = vec4(point_data.xy / 2.0 + 0.5, 1, 1);
}
"""

AUDIO_SIGNAL_FRAG_SHADER = """
varying vec4 f_color;

void main(void) {
    gl_FragColor = f_color;
}
"""


class FFTVisualizer(AlsaCanvas):
    def __init__(self, device=DEVICE, sample_rate=SAMPLE_RATE, period=PERIOD, window_size=WINDOW_SIZE):
        # TODO: Expose sample_rate, period, window_size
        super().__init__(device, sample_rate, period, window_size)

        self.audio_signal_program = gloo.Program(
            AUDIO_SIGNAL_VERT_SHADER, AUDIO_SIGNAL_FRAG_SHADER)
        self.audio_signal_program['point_data'] = np.ndarray(
            (0, 2), dtype=np.float32)
        self.audio_signal_program['u_scale'] = (1., 1.)

    def on_mouse_wheel(self, event):
        dx = np.sign(event.delta[1]) * .05
        scale_x, scale_y = self.program['u_scale']
        scale_x_new, scale_y_new = (scale_x * math.exp(2.5*dx),
                                    scale_y * math.exp(0.0*dx))
        self.audio_signal_program['u_scale'] = (
            max(1, scale_x_new), max(1, scale_y_new))
        self.update()

    def on_draw(self, event):
        gloo.clear()
        self.audio_signal_program.draw('line_strip')

    def on_data(self, event):
        all_data = self.pcm_buffer.data()
        if len(all_data) > 0:
            fft_data = np.fft.fft(all_data)
            fft_data = 10 * np.log10(fft_data.imag ** 2 + fft_data.real ** 2)
            fft_data /= np.max(np.abs(fft_data), axis=0)
            samples = len(all_data)
            x_data = (np.arange(samples) * 2 - samples) / samples
            point_data = np.stack((x_data, fft_data),
                                  axis=-1).astype(np.float32)
            self.audio_signal_program['point_data'] = point_data
            print(fft_data)

        self.update()


if __name__ == '__main__':
    vis = FFTVisualizer()
    app.run()
