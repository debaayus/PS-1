import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

"""
Necessary functions for scientists to create publication format images. Quite a bit of control in plotting is given to the user at different stages.
This code is absolutely reusable at all points of this project.
"""
def savetiff(fig, dirname, filename, dots_per_inch):
        fig_path=dirname+'/'+filename+'.tiff'
        png1 = BytesIO()
        fig.savefig(png1, format='png', dpi=float(dots_per_inch), bbox_inches='tight')

        # (2) load this image into PIL
        png2 = Image.open(png1)

        # (3) save as TIFF
        png2.save(fig_path)
        png1.close()
        return

def savepng(fig, dirname, filename, dots_per_inch):
        fig_path=dirname+'/'+filename+'.png'
        fig.savefig(fig_path, format='png', dpi=float(dots_per_inch), bbox_inches='tight')
        return
        


def savejpeg(fig, dirname, filename, dots_per_inch):
        fig_path=dirname+'/'+filename+'.jpeg'
        fig.savefig(fig_path, format='jpeg', dpi=float(dots_per_inch), bbox_inches='tight')
        return

def savepdf(fig, dirname, filename, dots_per_inch):
        fig_path=dirname+'/'+filename+'.pdf'
        fig.savefig(fig_path, format='pdf', dpi=float(dots_per_inch), bbox_inches='tight')
        return

def savecsv():
        pass

def savexlsx():
        pass








