from cProfile import Profile

import numpy as np

from ..classes.profile import ProfileHandler
from ..resources.language import Text


def load(path, type):

    """
    A function to load experimental results as lists,
    which returns them in the proper format to be plotted.
    """

    if type == "pdd":
        direction = "Z"
    else:
        direction = "X- {} Y".format(
            Text().orr[ProfileHandler().get_attribute("language")]
        )

    if path.endswith(".txt"):
        data = np.loadtxt(path, unpack=True)
    else:
        data = np.genfromtxt(path, delimiter=",", unpack=True)

    xvals, yvals = data[0], data[1]
    maximum = max(yvals)
    yvals = np.array([value / maximum for value in yvals])

    try:
        std_dev = data[2]
    except IndexError:
        std_dev = None

    return xvals, direction, yvals, std_dev
