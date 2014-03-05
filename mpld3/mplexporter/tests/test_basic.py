from ..exporter import Exporter
from ..renderers import ExampleRenderer

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


FAKE_OUTPUT = """
opening figure
  opening axes
    draw line with 20 points
    draw 10 markers
  closing axes
closing figure
"""


def test_fakerenderer():
    fig, ax = plt.subplots()
    ax.plot(range(20), '-k')
    ax.plot(range(10), '.k')

    renderer = ExampleRenderer()
    exporter = Exporter(renderer)
    exporter.run(fig)

    for line1, line2 in zip(renderer.output.strip().split(),
                            FAKE_OUTPUT.strip().split()):
        assert line1 == line2
