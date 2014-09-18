import unittest
import numpy as np
import matplotlib.pyplot as plt
import mpld3

class empty_collection_tests(unittest.TestCase):
    """ Ensure that mpld3renderer filters out empty line collections. """

    def test_extra_contour(self):
        """ Create an empty line collection by requesting invalid contours, and
        check that a collection with length(paths) === 0 is not passed to the
        JavaScript.
        """
        fig, ax = plt.subplots()
        X, Y = np.mgrid[0:5, 0:5]
        Z = X**2 - Y**2
        ax.contour(X, Y, Z, range(-15, 18, 2))  # last contour level is 17
                                                # but Z.max() is 16
        jsondict = mpld3.fig_to_dict(fig)

        for collection in jsondict["axes"][0]["collections"]:
            self.assertTrue(len(collection["paths"]) != 0)
        return

