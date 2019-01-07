import numpy as np
from vispy import gloo
from vispy import app

from alsa_canvas import AlsaCanvas


DEVICE = 'hw:Loopback,1'
SAMPLE_RATE = 44100
PERIOD = 1024
WINDOW_SIZE = PERIOD * 1

VERT_SHADER = """
attribute vec2 point_data;
varying vec4 f_color;
uniform vec2 u_scale;

void main () {
    gl_Position = vec4(point_data.x * u_scale.x,
                       point_data.y * u_scale.y, 0, 1);
    f_color = vec4(point_data.xy / 2.0 + 0.5, 1, 1);
}
"""

FRAG_SHADER = """
varying vec4 f_color;

void main(void) {
    gl_FragColor = f_color;
}
"""


class SignalVisualizer(AlsaCanvas):
    def __init__(self, device=DEVICE, sample_rate=SAMPLE_RATE, period=PERIOD, window_size=WINDOW_SIZE):
        super().__init__(device, sample_rate, period, window_size)
        self.program = gloo.Program(VERT_SHADER, FRAG_SHADER)
        self.program['point_data'] = np.ndarray((0, 2), dtype=np.float32)
        self.program['u_scale'] = (1., 1.)

    def on_data(self, event):
        all_data = self.pcm_buffer.data()
        all_data /= np.max(np.abs(all_data), axis=0)
        samples = len(all_data)
        x_data = (np.arange(samples) * 2 - samples) / samples
        point_data = np.stack((x_data, all_data), axis=-1).astype(np.float32)

        self.program['point_data'] = point_data
        self.update()


if __name__ == '__main__':
    vis = SignalVisualizer()
    app.run()
