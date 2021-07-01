import PySimpleGUI as sg
import pandas as pd 
import numpy as np
from input_gui import *



def data_input():
    
    home= landing_page.landing_page()

    while True:  # Event Loop
        event, values = home.read()

        if event == sg.WIN_CLOSED:  # if all windows were closed
            break
        if event == sg.WIN_CLOSED or event == 'Exit':
            home.close()
        if event == 'Browse':
            data, header_list,fn, filename=read_table.read_table()
            show_prompt = sg.popup_yes_no('Show the dataset?')
            if show_prompt=='Yes':
                skiprow, delim, filename=show_table.show_table(data, header_list, fn, filename)
                df, data_final, header_list_final, fn = read_table_final.read_table_final(skiprow, delim, filename)
                df, data_final, header_list_final, fn = show_table_final.show_table_final(df,data_final, header_list_final ,fn) #any index updates if needed
                return (df, data_final, header_list_final ,fn)
            else:
                break
    window.close()


if __name__ == '__main__':
    data_input()