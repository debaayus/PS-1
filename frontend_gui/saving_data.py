import PySimpleGUI as sg
import pandas as pd
import numpy as np
from frontend_gui.saving_utils import savecsv, savexlsx, savedatpdf


def save_data_dash(dm):
	layout1=[]