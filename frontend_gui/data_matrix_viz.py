import PySimpleGUI as sg
import pandas as pd 
import numpy as np
from tkinter.font import Font
from frontend_gui.saving_data import save_data_dash

def show_table(data, header_list, fn, filename):
	header_list = list(d0.columns)
    data = d0[0:].values.tolist()
    font_family, font_size = font = ('Helvetica', 10)
    sg.set_options(font=font)
    frm_input_layout = [
    [sg.Table(values=data, headings=header_list,
        enable_events=True, key='_TABLE_', 
        auto_size_columns=True,  justification='left',    
        hide_vertical_scroll=False, vertical_scroll_only=False, display_row_numbers=True
    )],
    [sg.Text('the true column header row number, please use the ROW column(the first column)', size=(45,5)), sg.Input(key='_IN1_', enable_events=True)],
    [sg.Text('Enter the delimiter visible, if any(eg: |, \\t, ;). If not visible please leave it blank', size=(45,2)), sg.Input(key='_IN2_', enable_events=True)],
    [sg.Submit()]]
    layout = [[sg.Frame('Input', frm_input_layout)]]

    window = sg.Window(fn, auto_size_text=True, auto_size_buttons=True,
                   grab_anywhere=True, resizable=False,
                   layout=layout, finalize=True,size=(800, 600))

    # Set real table width after here
    window.TKroot.update()
    tree = window['_TABLE_'].Widget
    tkfont = Font(family=font_family, size=font_size)
    data_array = np.array([header_list]+data)
    column_widths = [max(map(lambda item:tkfont.measure(item), data_array[:, i]))
    for i in range(data_array.shape[1])]
    for heading, width in zip(header_list, column_widths):
        tree.column(heading, width=width+font_size+20)

def dm_dash():
	pass



if __name__ == '__main__':
	dm_dash()
	