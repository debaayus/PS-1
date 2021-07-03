import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
from io import BytesIO

def draw_figure(canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg


def savetiff(figure, fig_name, path_to_folder):
        png1 = BytesIO()
        fig.savefig(png1, format='png')

        # (2) load this image into PIL
        png2 = Image.open(png1)

        # (3) save as TIFF
        png2.save(path_to_folder, fig_name)
        png1.close()

def savepng():
        pass


def savejpeg():
        pass








