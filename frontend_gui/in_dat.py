import PySimpleGUI as sg
import pandas as pd 
import numpy as np
from tkinter.font import Font



"""
The first page seen by the user when he starts the application.
08/07- More functionality of the home/landing page can be added and it can be made to look good
"""
def landing_page():

    layout2 = [[sg.Text('Press the button below to upload a csv file of a data matrix and to proceed to the visualization and multivaraite analysis of the data matrix', size=(50,5))],
    [sg.Button('Upload data matrix')]]

    layout3 = [[sg.Text('Press the button below to upload a csv file of the complete response data, i.e., resistance vs time/index data, and begin the full analysis pipeline', size=(50,5))],
    [sg.Button('Upload response data')]]

    layout=[
    [sg.Frame('Multivariate Analysis of Feature matrix', layout=layout2)], [sg.Frame('Full pipeline for analysis of response data', layout=layout3)],
    [sg.Button('Exit')]]
    return sg.Window('SMO sensor data analysis Toolbox', layout=layout, finalize=True, resizable=False, size=(500,400))



"""
The following function reads a csv file. It has error catching for 2 types of encoding. 
This is the first iteration of read table as initially, its shown with a default delimiter of a comma.
The second iteration allows the user to enter the delimiter which is visible
"""
def read_table():

    sg.set_options(auto_size_buttons=True)
    filename = sg.popup_get_file(
        'Dataset to read',
        title='Dataset to read',
        no_window=True, 
        file_types=(("CSV Files", "*.csv"),("Text Files", "*.txt"))) #accepts csv and txt files. 08-07: Needs to accept XLSX as well
    # --- populate table with file contents --- #
    if filename == '':
        return

    data = []
    header_list = [] #these two are created for displaying in a table format
    

    if filename is not None:
        fn = filename.split('/')[-1]
        try:
            d0 = pd.read_csv(filename, delimiter='\t')
        except:
            try:
                d0 = pd.read_csv(filename, encoding='utf-16', delimiter='\t')
            except:
                sg.popup_error('Error reading file in the read_table method. Click the error button to exit')
                return
        
        header_list = list(d0.columns)
        data = d0[0:].values.tolist()
        return (data, header_list,fn, filename)




"""
The following function displays the dataframe which has been created from the csv file.
It uses underlying Tkinter methods than pysimplegui itself as pysimplegui is not capable of adding a horizontal scroll bar.
A standard size of (800, 600) is maintained to be displayed in laptops without intruding background work
Font chosen is helvetica. This method allows the user to enter the visible delimiter apart from the usual comma.
"""
def show_table(data, header_list, fn, filename): 
  
    font_family, font_size = font = ('Helvetica', 10)
    sg.set_options(font=font)
    frm_input_layout = [
    [sg.Table(values=data, headings=header_list,
        enable_events=True, key='_TABLE_', 
        auto_size_columns=True,  justification='left',    
        hide_vertical_scroll=False, vertical_scroll_only=False, display_row_numbers=True
    )],
    [sg.Text('Enter the row number where the true column headers are located. Type X in the box if the header row(in white background) is the true column header. To find the true column header row number, please use the ROW column(the first column)', size=(45,5)), sg.Input(key='_IN1_', enable_events=True)],
    [sg.Text('Enter the delimiter visible, if any(eg: "|"pipe, ";" semi colon, ","comma, ":"colon). If not visible please leave it blank', size=(45,3)), sg.Input(key='_IN2_', enable_events=True)],
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
    
    while True:
        event, values= window.read()
        if event==sg.WIN_CLOSED:
            break
        if event=='Submit':
            try:
                window.close()
                return(values['_IN1_'], values['_IN2_'], filename)
            except:
                sg.popup_error('Error displaying table in the show_table method. Click the error button to exit.')
                break
    window.close()
    return




"""
This function definitely has some issues. The first of which is the problem of encoding. Most files are utf-8 however during testing, the author
ran into a file with encoding utf-16. Since, pandas doesn't automatically detect encodings. This particular usecase had to be hardcoded.
There might be an issue with only one file type i.e. a csv file with delimiter "\\t" and encoding utf-8 in which case the program will crash.

08-07: The author is still looking to solve this problem. This problem arises as pandas does not allow the read csv method to set the separator as None.
To counter the above problem, the author has to rely on the user. However, the tolist() method seems to catch the \\t delimiter without a hitch and displays it correctly. 
However the pandas csv method is unable to detect the \\t delimiter and is unable to detect an escape sequence to the aforementioned reason.
For the moment, its working fine with most files. Author plans to work out the issue or add a warning for the user to convert their files to utf-8 for usage.
"""

def read_table_final(skiprow, delim, filename):  
    if filename == '':
        sg.popup_error('Empty file. Click the error button to exit')
        return

    data_final = []
    header_list_final = []
    if skiprow is'X' or skiprow is 'x' or skiprow is '':
        skiprow=-1


    skip=int(skiprow)+1
    

    if filename is not None:
        
            fn = filename.split('/')[-1]
                                
            if delim is '': 
                try:
                    df = pd.read_csv(filename, skiprows=skip, encoding='utf-16', delimiter='\t') ##This line has been added as pandas is unable to detect encodings and delimiters
                except:
                    try:
                        df = pd.read_csv(filename, skiprows=skip) #for files with only comma
                    except:
                        sg.popup_error('Error reading file in the read_table_final method. Click the error button to exit')
                        return
                     
            else:
                try:
                    df = pd.read_csv(filename, skiprows=skip, delimiter=delim) #for files with delimiters apart from comma and \t utf-8
                except:
                    try:
                        df = pd.read_csv(filename, skiprows=skip, encoding='utf-16', delimiter=delim)
                    except:
                        sg.popup_error('Error reading file in the read_table_final method. Click the error button to exit')
                        return 
            header_list_final = list(df.columns) 
            data_final = df[0:].values.tolist()
            return (df,data_final, header_list_final ,fn)






"""
This function works fine. It relies on the user and their visual cues to interpret the data further. The method of displaying the table is similar 
to the show_table method i.e. usage of Tkinter methods instead of the wrapper
"""

def show_table_final(df,data_final, header_list_final ,fn): 
    font_family, font_size = font = ('Helvetica', 10)
    sg.set_options(font=font)
    frm_input_layout = [
    [sg.Table(values=data_final, headings=header_list_final,
        enable_events=False, key='_TABLE_', 
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
    
    t_col_no=''
    dat_col=''
    while True:
        event, values= window.read()
        if event==sg.WIN_CLOSED:
            break

        if event=='Submit':
            if values['_RAD_']==False:
                try:                       ##this particular block works to add an index column and set it as the index column for the dataframe object
                    df.insert(0, column='index', value=[int(x) for x in range(1, (df.shape[0]+1))])
                    header_list_final = list(df.columns)
                    data_final = df[0:].values.tolist()
                    t_col_no=sg.popup_get_text('Confirm the column number of the timestamp column (eg. Column number is 1 if the timestamp column is the 1st column. If no timestamp column, then please enter X', size=(15,7))
                    dat_col=sg.popup_get_text('Confirm the column number of the first sensor data. (eg. Column number is 2 if the first sensor data column is the 2nd column.)', size= (15,4))
                    df=df.set_index(df.columns[0])
                    header_list_final = list(df.columns)
                    data_final = df[0:].values.tolist()
                    window.close()
                    return (df, data_final, header_list_final ,fn, t_col_no, dat_col)
                except:
                    sg.popup_error('Error in index insertion method. Click the error button to exit')
                    break
            if values['_RAD_'] is True:
                t_col_no=sg.popup_get_text('Confirm the column number of the timestamp column (eg. Column number is 1 if the timestamp column is the 1st column. If no timestamp column, then please enter X', size=(15,7))
                dat_col=sg.popup_get_text('Confirm the column number of the first sensor data. (eg. Column number is 2 if the first sensor data column is the 2nd column.)', size= (15,4))
                df=df.set_index(df.columns[0])
                header_list_final = list(df.columns)
                data_final = df[0:].values.tolist()
                window.close()
                try:
                    t_col_mod=int(t_col_no)-1
                    t_col_no=str(t_col_mod)
                except:
                    pass
                dat_col_mod=int(dat_col)-1
                dat_col=str(dat_col_mod)
                return (df, data_final, header_list_final ,fn, t_col_no, dat_col) ##This returned data frame object is assumed to have an index based on the operations above

    window.close()
    return




"""
The following function is to allow an user to directly upload their data matrix and skip the response curve visualization and feature extraction module of the program.
"""
def show_table_MVA(dm, data_mat_final, header_list_mat_final, fn):
    font_family, font_size = font = ('Helvetica', 10)
    sg.set_options(font=font)
    frm_table_layout = [
    [sg.Table(values=data_mat_final, headings=header_list_mat_final,
        enable_events=False, key='_TABLE_', 
        auto_size_columns=True,  justification='left',    
        hide_vertical_scroll=False, vertical_scroll_only=False, display_row_numbers=False
    )]]
    
    param=[[sg.Text('Confirm the type of matrix:')], 
    [sg.Radio('Type I', "type", default=True, key='_TYPE_'),
    sg.Radio('Type II', "type", default=False)]]
    
    
    layout = [[sg.Frame('Input', frm_table_layout)],
    [sg.Frame('Type of matrix', layout=param), sg.Text('If you missed entering your delimiter, please restart the program', size=(50,1))], 
    [sg.Button('Proceed to Multivariate Analysis')]]

    window = sg.Window(fn, auto_size_text=True, auto_size_buttons=True,
                   grab_anywhere=True, resizable=False,
                   layout=layout, finalize=True,size=(800, 600))

# Set real table width after here
    window.TKroot.update()
    tree = window['_TABLE_'].Widget
    tkfont = Font(family=font_family, size=font_size)
    data_array = np.array([header_list_mat_final]+data_mat_final)
    column_widths = [max(map(lambda item:tkfont.measure(item), data_array[:, i]))
    for i in range(data_array.shape[1])]
    for heading, width in zip(header_list_mat_final, column_widths):
        tree.column(heading, width=width+font_size+20)

    while True:
        event, values= window.read()
        if event==sg.WIN_CLOSED:
            break

        if event=='Proceed to Multivariate Analysis':
            if values['_TYPE_']==False:
                feature=t2(dm)
                window.close()
                return (dm, 2, fn, feature)
            else:
                sensor_name=t1(dm)
                window.close()
                return (dm, 1, fn, sensor_name)
    window.close()
    return

def t1(dm):
    layout=[[sg.popup_get_text('Enter the name of the sensor for your Type I matrix'), sg.Input(key='_SENSORNAME_', enable_events=True)],
    [sg.Button('Proceed directly to MVA')]]
    
    layout2= [[sg.Text('If you wish to visualize concentration and a feature in a plot, please enter the following parameters')],
    [sg.Text('Enter the concentration values in sequence separated by commas. The number of values entered must match the number of rows in your Type I matrix')],
    [sg.Text('Expected number of parameters are')],
    [sg.Input(key='_CONC_', enable_events=True)],
    [sg.Button('Plot feature and concentration')]]
    return

def t2(dm):
    features=['Sensitivity','Recovery Slope', 'Response Slope', 'Recovery Time', 'Response Time', 'Integral Area']
    layout=[
    [sg.Text('Choose the feature which has been tabulated in your uploaded Type II data matrix')],
    [sg.Combo(values=features, default_value=features[0], key='_FEATURE_', size=(30, 6), readonly=True)],
    [sg.Button('Submit')]]
    window=sg.Window('Type II feature', layout=layout)

    while True:
        event, values=window.read()
        if event==sg.WIN_CLOSED:
            break
        if event=='Submit':
            window.close()
            return values['_FEATURE_']
    window.close()
    return









"""
This is the main function which controls the event loops and program sequence for the input part of the GUI.
"""
def data_input():
    
    home= landing_page()

    while True:  # Event Loop
        event, values = home.read()

        if event == sg.WIN_CLOSED or event == 'Exit':  # if all windows were closed
            break
        elif event == 'Upload response data':
            data, header_list,fn, filename=read_table()
            show_prompt = sg.popup_yes_no('Process the sensor response data?')
            if show_prompt=='Yes':
                home.close()
                skiprow, delim, filename=show_table(data, header_list, fn, filename)
                df, data_final, header_list_final, fn = read_table_final(skiprow, delim, filename)
                df, data_final, header_list_final, fn, t_col_no, dat_col = show_table_final(df,data_final, header_list_final ,fn) #any index updates if needed
                return (df, data_final, header_list_final ,fn, t_col_no, dat_col)
            else:
                break
        elif event=='Upload data matrix':
            data, header_list,fn, filename=read_table()
            show_prompt = sg.popup_yes_no('Process the feature matrix?')
            if show_prompt=='Yes':
                home.close()
                skiprow, delim, filename=show_table(data, header_list, fn, filename)
                df, data_final, header_list_final, fn = read_table_final(skiprow, delim, filename)
                dm, typemat, fn, sens_name_or_feature = show_table_MVA(df, data_final, header_list_final ,fn) 
                return (dm, typemat, fn, sens_name_or_feature)
            else:
                break

    home.close()
    return


if __name__ == '__main__':
    data_input()