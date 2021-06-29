import PySimpleGUI as sg
import pandas as pd 
import numpy as np
from tkinter.font import Font

def landing_page():
    layout = [[sg.Text('Hello World')],
              [sg.Text('Press the browse button to attach .CSV or .XLSX file')],
              [sg.Button('Browse'), sg.Button('Exit')]]
    return sg.Window('Welcome', layout, finalize=True, resizable=True)



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
            if True:
                try:
                    d0 = pd.read_csv(filename)
                    header_list = list(d0.columns)
                    data = d0[0:].values.tolist()
                    return (d0,data, header_list,fn, filename)
                except:
                    d0 = pd.read_csv(filename, encoding='utf-16')
                    header_list = list(d0.columns)
                    data = d0[0:].values.tolist()
                    return (d0,data, header_list,fn, filename)
            
        except:
            sg.popup_error('Error reading file. Click the error button to exit')
            return


def show_table(d0, data, header_list, fn, filename): ### Col_index not yet integrated
  
    font_family, font_size = font = ('Helvetica', 11)
    sg.set_options(font=font)
    frm_input_layout = [
    [sg.Table(values=data, headings=header_list,
        enable_events=True, key='_TABLE_', 
        auto_size_columns=True,  justification='left',    
        hide_vertical_scroll=False, vertical_scroll_only=False, display_row_numbers=True, pad=(25,25)
    )],
    [sg.Text('Enter the row number where the true column headers are located. Enter 0 if the header row(in white) is the true column header', size=(45,2)), sg.Input(key='_IN1_', enable_events=True)],
    [sg.Text('Enter the delimiter visible, if any(eg: |, \\t, ;)'), sg.Input(key='_IN2_', enable_events=True)],
    [sg.Text("Enter index column number i.e., 0 for the first column. If there isn't any index then leave the field blank, an index will be created", size=(45,3)), sg.Input(key='_IN3_', enable_events=True)],
    [sg.Button('Submit')]]
    layout = [[sg.Frame('Input', frm_input_layout)]]

    window = sg.Window(fn, auto_size_text=True, auto_size_buttons=True,
                   grab_anywhere=False, resizable=False,
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
    
    while True:
        event, values= window.read()
        if event==sg.WIN_CLOSED:
            break
        if event=='Submit':
            window.close()
            read_table_final(values['_IN1_'], values['_IN2_'], values['_IN3_'], d0, filename) ### Col_index not yet integrated
            

def read_table_final(skiprow, delim, index_col, d0, filename): ### Col_index not yet integrated. 
    if filename == '':
        sg.popup_error('Empty file. Click the error button to exit')
        return

    data_final = []
    header_list_final = []

    skip=int(skiprow)+1
    

    if filename is not None:
        try:
            fn = filename.split('/')[-1]
                                
            if delim is '': ### Col_index not yet integrated
                try:
                    
                    df = pd.read_csv(filename, skiprows=skip) ##dataframe read working fine
                    header_list = list(df.columns)
                    data_final = df[0:].values.tolist()
                    show_table_final(df,data_final, header_list_final ,fn) ### Col_index not yet integrated
                except:
                    
                    df = pd.read_csv(filename, encoding='utf-16', skiprows=skip) ### Col_index not yet integrated
                    header_list = list(df.columns)
                    data = df[0:].values.tolist()
                    show_table_final(df,data_final, header_list_final ,fn) 
            else:
                try:
                    print("Here delim")
                    df = pd.read_csv(filename, skiprows=skip, delimiter=delim) ### Col_index not yet integrated
                    header_list = list(df.columns)
                    data_final = df[0:].values.tolist()
                    show_table_final(df,data_final, header_list_final ,fn)
                    
                except:
                    print("Here delim")
                    df = pd.read_csv(filename, encoding='utf-16', skiprows=skip, delimiter=delim) ### Col_index not yet integrated
                    header_list = list(df.columns)
                    data = df[0:].values.tolist()
                    show_table_final(df,data_final, header_list_final ,fn)
        except:
            sg.popup_error('Error reading file. Click the error button to exit')
            return


def show_table_final(df,data_final, header_list_final ,fn): ###Not working
    layout = [
        [sg.Table(values=data_final,
                  headings=header_list_final,
                  font='Helvetica',
                  pad=(25,25),
                  display_row_numbers=False,
                  auto_size_columns=True,
                  num_rows=min(25, len(data_final)))],
        [sg.Text('Confirm the above dataframe for further computation'), sg.Button('Confirm')]
    ]

    print(data_final[0])

    window = sg.Window(fn, layout, grab_anywhere=False, resizable=False)
    event, values = window.read()
    window.close()
    while True:
        event, values= window.read()
        if event==sg.WIN_CLOSED:
            break
        if event=='Confirm':
            window.close()
            feature_extraction(df, filename)### Not a real function just a placeholder.
            



def main():
    
    home= landing_page()

    while True:  # Event Loop
        event, values = home.read()

        if event == sg.WIN_CLOSED:  # if all windows were closed
            break
        if event == sg.WIN_CLOSED or event == 'Exit':
            home.close()
        if event == 'Browse':
            d0,data, header_list,fn, filename=read_table()
            show_prompt = sg.popup_yes_no('Show the dataset?')
            if show_prompt=='Yes':
                show_table(d0, data, header_list, fn, filename)


if __name__ == '__main__':
    main()