import PySimpleGUI as sg
import pandas as pd 
import numpy as np
from tkinter.font import Font

def show_table_final(df,data_final, header_list_final ,fn): 
    font_family, font_size = font = ('Helvetica', 10)
    sg.set_options(font=font)
    frm_input_layout = [
    [sg.Table(values=data_final, headings=header_list_final,
        enable_events=True, key='_TABLE_', 
        auto_size_columns=True,  justification='left',    
        hide_vertical_scroll=False, vertical_scroll_only=False, display_row_numbers=False
    )],
    [sg.Text('Select YES if index column(first column with values 1, 2 ,3) is visible. Select NO to allow the program to create an index column', size=(50,5)), 
    sg.Radio('Yes', "yesorno", default=True, key='_RAD_'),
    sg.Radio('No', "yesorno", default=False)],
    [sg.Text('If you missed entering your delimiter, please restart the program', size=(50,1))], 
    [sg.Text('Press submit to confirm the above dataframe for further computation', size=(50,1))],
    [sg.Submit()]]
    layout = [[sg.Frame('Input', frm_input_layout)]]

    window = sg.Window(fn, auto_size_text=True, auto_size_buttons=True,
                   grab_anywhere=True, resizable=False,
                   layout=layout, finalize=True,size=(800, 600))

# Set real table width after here
    window.TKroot.update()
    tree = window['_TABLE_'].Widget
    tkfont = Font(family=font_family, size=font_size)
    data_array = np.array([header_list_final]+data_final)
    column_widths = [max(map(lambda item:tkfont.measure(item), data_array[:, i]))
    for i in range(data_array.shape[1])]
    for heading, width in zip(header_list_final, column_widths):
        tree.column(heading, width=width+font_size+20)
    
    while True:
        event, values= window.read()
        if event==sg.WIN_CLOSED:
            break

        if event=='Submit':
            if values['_RAD_']==False:
                try:
                    df.insert(0, column='index', value=[x for x in range(1, (df.shape[0]+1))])
                    header_list_final = list(df.columns)
                    data_final = df[0:].values.tolist()
                except:
                    sg.popup_error('Error in index insertion method. Click the error button to exit')
                    break
                try:
                    window.close()
                    show_table_final(df, data_final, header_list_final ,fn)
                except:
                    sg.popup_error('Error in calling show_table method again. Click the error button to exit')
            return (df, data_final, header_list_final ,fn)
            break
    window.close()
    return

if __name__ == '__main__':
    show_table_final()