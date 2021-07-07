import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO


def savetiff(fig, fig_name, path_to_folder):
        png1 = BytesIO()
        fig.savefig(png1, format='png')

        # (2) load this image into PIL
        png2 = Image.open(png1)

        # (3) save as TIFF
        png2.save(path_to_folder, fig_name)
        png1.close()

def savepng(fig, fig_path, dots_per_inch):
        fig_nm=fig_path+'.png'
        fig.savefig(fig_nm, format='png', dpi=dots_per_inch)
        return
        


def savejpeg():
        pass








