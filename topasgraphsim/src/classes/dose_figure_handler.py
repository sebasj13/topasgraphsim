import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.ticker import AutoMinorLocator
from PIL import Image, ImageTk
from win32api import GetSystemMetrics

from ..functions.plot_args import plot_args


class DoseFigureHandler:
    def __init__(self):

        plt.style.use("default")
        self.colors = [
            ["go", "bo", "ro", "co", "mo"],
            ["green", "blue", "red", "cyan", "magenta"],
        ]

        self.fig = Figure(figsize=(10, 5), constrained_layout=True, dpi=600)

        self.canvas = FigureCanvasAgg(self.fig)

        self.ax = self.fig.add_subplot(111)

        self.props = dict(boxstyle="round", facecolor="wheat", alpha=0.6)
        self.filepaths = []
        self.filenames = []
        self.data = []

    def flush(self):

        self.filepaths = []
        self.filenames = []
        self.data = []

    def fits(self, image):

        """
        A function that scales an image to the width of the screen.
        """

        scr_width = GetSystemMetrics(0)
        width = int(scr_width)
        scale_factor = image.shape[1] / width
        image = cv2.resize(
            image,
            (width, int(image.shape[0] / scale_factor)),
            interpolation=cv2.INTER_AREA,
        )

        return image

    def set_axis(self):

        self.ax.clear()
        self.ax.grid(True, which="major")
        self.ax.grid(True, which="minor", color="grey", linewidth=0.1)
        self.ax.xaxis.set_minor_locator(AutoMinorLocator())
        self.ax.yaxis.set_minor_locator(AutoMinorLocator())
        self.ax.tick_params(axis="both", which="minor", length=2)

    def add_plot_data(self, datanames):

        for tuple in datanames:
            filename = tuple[0]
            type = tuple[1]
            if filename not in self.filepaths:
                self.filepaths += [filename]
                self.data += [plot_args(filename, type)]
                self.filenames += [filename.split("/")[-1]]

    def add_legend(self):

        self.ax.legend(
            loc="upper right",
            framealpha=0.6,
            facecolor="wheat",
            edgecolor="black",
            fancybox=True,
        )

    def add_descriptors(self):

        for index, plot_data in enumerate(self.data):

            if len(plot_data) == 7:
                Q, dQ, zmax = plot_data[4], plot_data[5], plot_data[6]
                textstr = "Q     = {} ± {}\n{} = {} mm".format(Q, dQ, "$z_{max}$", zmax)
                self.ax.text(
                    0.795,
                    0.7 - 0.1 * index,
                    textstr,
                    transform=self.ax.transAxes,
                    fontsize=10,
                    verticalalignment="top",
                    bbox=self.props,
                    color=self.colors[1][index],
                )
            else:
                (
                    HWB,
                    CAXdev,
                    flat_krieger,
                    flat_stddev,
                    S,
                    Lpenumbra,
                    Rpenumbra,
                    Lintegral,
                    Rintegral,
                ) = (
                    plot_data[4],
                    plot_data[5],
                    plot_data[6],
                    plot_data[7],
                    plot_data[8],
                    plot_data[9],
                    plot_data[10],
                    plot_data[11],
                    plot_data[12],
                )
                textstr = "HWB = {} mm\n{} = {} mm\n{} = {}\n{} = {}\n{} = {} mm\n{} = {} mm\n{} = {}\n{} = {}\nSymmetrie = {}".format(
                    HWB,
                    "$CAX_{dev}$",
                    CAXdev,
                    "$FLAT_{Krieger}$",
                    flat_krieger,
                    "$FLAT_{stddev}$",
                    flat_stddev,
                    "$Penumbra_{L}$",
                    Lpenumbra,
                    "$Penumbra_{R}$",
                    Rpenumbra,
                    "$Integral_{L}$",
                    Lintegral,
                    "$Integral_{R}$",
                    Rintegral,
                    S,
                )

                self.ax.text(
                    0.5,
                    0.5,
                    textstr,
                    transform=self.ax.transAxes,
                    fontsize=10,
                    verticalalignment="top",
                    bbox=self.props,
                    horizontalalignment="center",
                    color=self.colors[1][index],
                )

    def set_x_label(self):

        xlabel = "{}-Achse [mm]".format(self.data[0][1])
        self.ax.set_xlabel(xlabel, size=12)

    def create_plots_from_data(self):

        for index, plot_data in enumerate(self.data):
            self.ax.errorbar(
                x=plot_data[0],
                y=plot_data[2],
                yerr=plot_data[3],
                fmt=self.colors[0][index],
                ecolor="r",
                elinewidth=0.5,
                capsize=1,
                capthick=0.2,
                ms=2,
                label=f"{self.filenames[index]}",
            )
            self.ax.plot(
                plot_data[0],
                plot_data[2],
                "-.",
                color=self.colors[1][index],
                linewidth=0.5,
            )

    def return_figure(self, filenames):

        self.set_axis()
        self.add_plot_data(filenames)
        self.set_x_label()
        self.create_plots_from_data()
        self.add_legend()
        self.add_descriptors()

        self.canvas.draw()
        buffer = self.canvas.buffer_rgba()
        image_array = np.asarray(buffer)
        fit_array = self.fits(image_array)
        image = Image.fromarray(fit_array)
        photoimage = ImageTk.PhotoImage(image)

        return photoimage, self.data[0][1]
