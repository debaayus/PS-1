import PySimpleGUI as sg
import pandas as pd 
import numpy as np

def read_table():

    sg.set_options(auto_size_buttons=True)
    filename = sg.popup_get_file(
        'Dataset to read',
        title='Dataset to read',
        no_window=True, 
        file_types=(("CSV Files", "*.csv"),("Text Files", "*.txt")))
    # --- populate table with file contents --- #
    if filename == '':
        return

    data = []
    header_list = []
    

    if filename is not None:
        fn = filename.split('/')[-1]
        try:
            d0 = pd.read_csv(filename)
        except:
            try:
                d0 = pd.read_csv(filename, encoding='utf-16')
            except:
                sg.popup_error('Error reading file in the read_table method. Click the error button to exit')
                return
        
        header_list = list(d0.columns)
        data = d0[0:].values.tolist()
        return (data, header_list,fn, filename)


if __name__ == '__main__':
    read_table()
            
            