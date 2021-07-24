import PySimpleGUI as sg
import pandas as pd
import numpy as np
from frontend_gui.saving_utils import savecsv, savexlsx, savetxt


def save_data_dash(dm):
    dirname = sg.popup_get_folder('Please choose a folder to save the data matrix')

    combolayout=[[sg.Combo(['CSV', 'XLSX', 'TXT'], default_value='CSV', readonly=True, key='-LB-')]]

    layout=[[sg.Text('Enter the filename', size=(45,1)), sg.Input(default_text='data matrix', key='_FN_', enable_events=True)],
    [sg.Text('Enter separator. Default value is comma', size=(45,1)), sg.Input(key='_SEP_', enable_events=True)],   ##DPI extremely necessary
    [sg.Frame('Choose format', layout=combolayout)],
    [sg.Text('Default encoding chosen is "utf-8" for readability reasons')],
    [sg.Text('Click "Save" to save the plot and "Exit" to quit the dataframe saving dashboard', size=(60,1))],
    [sg.Button('Save'), sg.Button('Exit')]]

    window=sg.Window('Save data matrix', layout=layout, size=(800,300))##figure out if we can make multiple file saves work or just go for single save and then returning to the original plot


    while True:
        event, values = window.Read()
        if event==sg.WIN_CLOSED or event=='Exit':
            break
        if event == 'Save':
            if values['_SEP_'] is '':
                values['_SEP_']=','
            if values['_FN_'] is '':
                sg.popup_error('Filename field empty')
                continue
            if values['-LB-']=='CSV':
                savecsv(dm, dirname, values['_FN_'], values['_SEP_'])
                break
            elif values['-LB-']=='XLSX':
                savexlsx(dm, dirname, values['_FN_'])
                break
            elif values['-LB-']=='TXT':
                savetxt(dm, dirname, values['_FN_'], values['_SEP_'])
                break
            


    window.close()
    return