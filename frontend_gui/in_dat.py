import sys, os
import PySimpleGUI as sg
import pandas as pd 
import numpy as np
from tkinter.font import Font
from frontend_gui.data_matrix_viz import options



"""
The first page seen by the user when he starts the application.
08/07- More functionality of the home/landing page can be added and it can be made to look good
"""
def resource_path(relative_path):
    #Get the absolute path to the resource, works for dev and for PyInstaller
        try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


def landing_page():

    
    hello='This application will allow users to extract features from the response data of their sensor array. It also provides the user, the option to upload their own pre-determined data matrix. After extracting features and creating the data matrix, the application aims to provide analysis and plotting tools at various stages. The whole package has been built with open source software, namely Python. The GUI of the application has been built with PySimpleGUI, an open source library which acts as a wrapper for a popular Python GUI building library, Tkinter. The other functions of this app are supported by popular Python libraries: Pandas, MatPlotLib, NumPy, SciPy, Pillow and Scikit-Learn.'
    
    intro=[[sg.Text('Application designed by: \nDebaayus Swain(2019B2A30983P)\nKunal Gupta(2019A3PS0229P)\n\nUnder the guidance of:\nDr. A. Sree Rama Murthy, NCSS, MCD, MC&MFCG, IGCAR, Kalpakkam\n\nAt Indira Gandhi Centre for Atomic Research, Kalpakkam,\n\nA Practice School-I station of Birla Institute of Technology and Science, Pilani', size=(80,12))],
    [sg.Image(filename='IGCAR_logo.png', pad=((100,100),(20,0))), sg.Image(filename='bits.png', pad=((100, 100),(20,0)))]]

    disclaimer=[[sg.Text('The Authors do not warrant the functions contained in the program will meet your requirements or that the operation of the program will be uninterrupted or error-free.', size=(80,3))]]
    
    
    home_tab_layout=[
    [sg.Text('Welcome to the SMO Sensing Toolbox', font=('Helvetica', 14))],
    [sg.Text(hello, size=(83,8))],
    [sg.Text('At the time of release, the application supports time varying response of static gas injections with pre-defined indices for point of injections (POIs). Further releases might support dynamic responses even with unindexed points of injection.', size=(80,3))],
    [sg.Image(filename=resource_path('IGCAR_logo.png'), pad=((100,100),(20,0))), sg.Image(filename=resource_path('bits.png'), pad=((100, 100),(20,0)))]]

    layout2 = [[sg.Text('This tab is designed for a customised feature matrix.')],
    [sg.Text('Type I (All Features One Sensor): All the features are extracted for a single chosen sensor (based on the points of injection provided)', size=(80, 3))],
    [sg.Text('Type II (One Feature All Sensors): One chosen feature is extracted for multiple sensors (based on the points of injection provided)', size=(80,6))],
    [sg.Text('The following are the features available in the extraction module', size=(80,1))],
    [sg.Multiline("1. Response% : Differential signal normalised with respect to baseline.\n2. Response slope: Maximum rate of change of signal during response.\n3. Recovery slope: Maximum rate of change of signal during recovery.\n4. Response time: The time required for 90% response of sensor signal in seconds.\n5. Recovery time: The time taken for 90% recovery of sensor signal in seconds.\n6. Integral area: Area of the signal swept between between the times of point of injection and user defined value in seconds.", disabled=True, size=(80, 8))],
    [sg.Text('', size=(80,5))],
    [sg.Text('Press the button below to upload a csv file of a data matrix and proceed to the visualization and multivariate analysis of the data matrix', size=(80,2))],
    [sg.Button('Upload data matrix')]]

    header_response=['Scan', 'Timestamp', 'Sensor 1', 'Sensor 2', 'Sensor 3']
    data_response=[['1','0', '133', '677', '391'], 
    ['2','2', '134', '624', '380'], 
    ['3','4', '135', '663', '385'], 
    ['4','6', '133', '639', '343'], 
    ['5','8', '133', '673', '391'],
    ['6','10', '137', '342', '392'],
    ['7','12', '138', '602', '367'],
    ['8','14', '136', '671', '376'],
    ['9','16', '136', '678', '397'],
    ['10','18', '139', '667', '369'],
    ['11','20', '133', '673', '391'],
    ['12','22', '133', '780', '391']]


    layout3 = [[sg.Text('This tab is designed for resistance vs time data from the sensor array. The data can have multiple sensors with a timestamp column to determine their time varying behaviour. The signals are expected to be noisy, however with the user providing the points of injection, the application algorithm does not have to deal with the noise', size=(84,6))],
    [sg.Text('This is an example of the expected data:')],
    [sg.Table(values=data_response, headings=header_response, hide_vertical_scroll=False, vertical_scroll_only=False,
        enable_events=False, auto_size_columns=True,  justification='left', display_row_numbers=False)],
    [sg.Text('', size=(80, 5))],
    [sg.Text('Press the button below to upload a csv file of the complete response data, i.e., resistance vs time/index data, and begin the full analysis pipeline', size=(80,2))],
    [sg.Button('Upload response data')]]

    layout=[
    [sg.TabGroup([[sg.Tab('Home', layout=home_tab_layout)], [sg.Tab('Multivariate Analysis of Feature Matrix', layout=layout2)], [sg.Tab('Full pipeline for analysis of response data', layout=layout3)], [sg.Tab('Author Information', layout=intro)], [sg.Tab('Disclaimer', layout=disclaimer)]])],
    [sg.Button('Exit')]]
    return sg.Window('SMO sensor data analysis Toolbox', layout=layout, finalize=True, resizable=False, size=(1000, 700))



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
        hide_vertical_scroll=False, vertical_scroll_only=False, display_row_numbers=True, size=(100, 20)
    )],
    [sg.Text('Enter the row number where the true column headers are located. Type X in the box if the header row(in white background) is the true column header. To find the true column header row number, please use the ROW column(the first column)', size=(70,4)), sg.Input(key='_IN1_', enable_events=True)],
    [sg.Text('Enter the delimiter visible, if any(eg: "|"pipe, ";" semi colon, ","comma, ":"colon). If not visible please leave it blank', size=(70,3)), sg.Input(key='_IN2_', enable_events=True)],
    [sg.Submit()]]
    layout = [[sg.Frame('Input', frm_input_layout)]]
    
    
    
    window = sg.Window(fn, auto_size_text=True, auto_size_buttons=True,
                   grab_anywhere=True, resizable=False,
                   layout=layout, finalize=True,size=(1200, 800))


  

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
        hide_vertical_scroll=False, vertical_scroll_only=False, display_row_numbers=False, size=(100, 20)
    )]]
    param=[[sg.Text('Select YES if index column(first column with values 1, 2 ,3) is visible. Select NO to allow the program to create an index column', size=(70,2)), 
    sg.Radio('Yes', "yesorno", default=True, key='_RAD_'),
    sg.Radio('No', "yesorno", default=False)],
    [sg.Text('Enter the column number of the timestamp column (eg. Column number is 2 if the timestamp column is the 2nd column(if index is 1st column)). If no timestamp column, then please enter X', size=(70,3)), sg.Input(key='_TCOL_', enable_events=True)],
    [sg.Text('Enter the column number of the first sensor data. (eg. Column number is 3 if the first sensor data column is the 3rd column(if index and timestamp are the first 2 columns.))', size=(70,2)), sg.Input(key='_DATCOL_', enable_events=True)]]
    
    layout = [[sg.Frame('Input', frm_input_layout)],
    [sg.Frame('Parameters from visual inspection', layout=param)],
    [sg.Text('If you missed entering your delimiter, please restart the program', size=(50,1))], 
    [sg.Text('Press submit to confirm the above dataframe for further computation', size=(50,1))],
    [sg.Submit()]]

    window = sg.Window(fn, auto_size_text=True, auto_size_buttons=True,
                   grab_anywhere=True, resizable=False,
                   layout=layout, finalize=True,size=(1200, 800))

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
            if values['_TCOL_'] is '' or values['_DATCOL_'] is '':
                sg.popup_error('Timestamp column field or first sensor column field empty')
                continue
            if values['_RAD_']==False:
                try:                       ##this particular block works to add an index column and set it as the index column for the dataframe object
                    df.insert(0, column='index', value=[int(x) for x in range(1, (df.shape[0]+1))])
                    header_list_final = list(df.columns)
                    data_final = df[0:].values.tolist()
                    t_col_no=values['_TCOL_']
                    dat_col=values['_DATCOL_']
                    df=df.set_index(df.columns[0])
                    header_list_final = list(df.columns)
                    data_final = df[0:].values.tolist()
                    window.close()
                    return (df, data_final, header_list_final ,fn, t_col_no, dat_col)
                except:
                    sg.popup_error('Error in index insertion method. Click the error button to exit')
                    break
            elif values['_RAD_'] is True:
                t_col_no=values['_TCOL_']
                dat_col=values['_DATCOL_']
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
        hide_vertical_scroll=False, vertical_scroll_only=False, display_row_numbers=False, size=(100, 15)
    )]]
    
    
    indexlayout=[[sg.Text('Select YES if index column(analyte names, signal numbers or integers) of the data matrix is visible. Select NO to allow the program to create an index column', size=(70,6)), 
    sg.Radio('Yes', "yesorno", default=True, key='_RAD_'),
    sg.Radio('No', "yesorno", default=False)]]
    
    
    basic_layout = [[sg.Frame('Input', frm_table_layout)],
    [sg.Frame('Index confirmation', layout=indexlayout)],
    [sg.Text('If you missed entering your delimiter, please restart the program', size=(70,1))]] 

    type1_layout1=[[sg.Text('Enter the name of the sensor for your Type I matrix'), sg.Input(key='_SENSORNAME_', enable_events=True)]]
    
    
    type1_layout=[[sg.Frame('MVA parameters(Mandatory)', layout=type1_layout1)],
    [sg.Text('Press data matrix dashboard to insert columns, change indexing, visualize plots and then proceed to the ML algorithm applications', size=(70,2))],
    [sg.Button('Data matrix action dashboard for Type I')]]
    
    features=['Response(in %)','Response Slope', 'Recovery Slope', 'Response Time', 'Recovery Time', 'Integral Area','Ratio']
    type2_layout1=[
    [sg.Text('Choose the feature which has been tabulated in your uploaded Type II data matrix')],
    [sg.Combo(values=features, default_value=features[0], key='_FEATURE_', size=(30, 7), readonly=True)]]
    
    type2_layout=[[sg.Frame('MVA parameters(Mandatory)', layout=type2_layout1)],    
    [sg.Text('Press data matrix dashboard to insert columns, change indexing, visualize plots and then proceed to the ML algorithm applications', size=(70,2))],
    [sg.Button('Data matrix action dashboard for Type II')]]

    explainertab=[[sg.Text('Type I(All Features One Sensor): All the features are extracted for a single chosen sensor (based on the points of injection provided)')],
    [sg.Text('Type II(One Feature All Sensors): One chosen feature is extracted for multiple sensors (based on the points of injection provided)')],
    [sg.Text('', size=(80,3))],
    [sg.Text('The following are the features available in the extraction module', size=(80,1))],
    [sg.Multiline("1. Response% : Differential signal normalised with respect to baseline.\n2. Response slope: Maximum rate of change of signal during response.\n3. Recovery slope: Maximum rate of change of signal during recovery.\n4. Response time: The time required for 90% response of sensor signal in seconds.\n5. Recovery time: The time taken for 90% recovery of sensor signal in seconds.\n6. Integral area: Area of the signal swept between between the times of point of injection and user defined value in seconds.", disabled=True, size=(80, 8))]]

    layout=[[sg.TabGroup([[sg.Tab('Explanation', layout=explainertab)], [sg.Tab('Feature matrix display', layout=basic_layout)], [sg.Tab('Type I matrix', layout=type1_layout)], [sg.Tab('Type II matrix', layout=type2_layout)] ])]]

    window = sg.Window(fn, auto_size_text=True, auto_size_buttons=True,
                   grab_anywhere=True, resizable=False,
                   layout=layout, finalize=True,size=(1200, 600))

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

        if event=='Data matrix action dashboard for Type I':
            if values['_RAD_']==False:
                try:                       ##this particular block works to add an index column and set it as the index column for the dataframe object
                    dm.insert(0, column='index', value=[int(x) for x in range(1, (dm.shape[0]+1))])
                    dm=dm.set_index(dm.columns[0])
                except:
                    sg.popup_error('Error in index insertion method. Click the error button to exit')
                    continue
                if values['_SENSORNAME_'] is '':
                    sg.popup_error('Sensor name field is empty in Type I tab')
                    continue
                window.close()
                dm=options(dm, 0, 1)
                return (dm, 1, values['_SENSORNAME_'])
            else:
                try:
                    dm=dm.set_index(dm.columns[0])
                except:
                    sg.popup_error('Error in index setting')
                    continue
                if values['_SENSORNAME_'] is '':
                    sg.popup_error('Sensor name field is empty in Type I tab')
                    continue
                window.close()
                dm=options(dm,0,1)
                return (dm, 1, values['_SENSORNAME_'])


        elif event=='Data matrix action dashboard for Type II':
            if values['_RAD_']==False:
                try:                       ##this particular block works to add an index column and set it as the index column for the dataframe object
                    dm.insert(0, column='index', value=[int(x) for x in range(1, (dm.shape[0]+1))])
                    dm=dm.set_index(dm.columns[0])
                except:
                    sg.popup_error('Error in index insertion method. Click the error button to exit')
                    continue
                sg.popup('Please confirm the feature chosen: {}'.format(values['_FEATURE_']))
                window.close()
                dm=options(dm, 0, 2)
                return (dm, 2, values['_FEATURE_'])
            else:
                try:
                    dm=dm.set_index(dm.columns[0])
                except:
                    sg.popup_error('Error in index setting')
                    continue
                sg.popup('Please confirm the feature chosen: {}'.format(values['_FEATURE_']))
                window.close()
                dm=options(dm, 0, 2)
                return (dm, 2, values['_FEATURE_'])
                

            
    window.close()
    return


"""
def t1(dm, fn):
    layout1=[[sg.Text('Enter the name of the sensor for your Type I matrix'), sg.Input(key='_SENSORNAME_', enable_events=True)],
    [sg.Button('Proceed directly to application of machine learning algorithms')]]
    
    
    layout=[[sg.Frame('MVA parameters(Mandatory)', layout=layout1)],
    [sg.Text('Press data matrix dashboard to insert columns, change indexing, visualize plots and then proceed to the ML algorithm applications', size=(50,2))],
    [sg.Button('Data matrix action dashboard')]]

    window=sg.Window('Type I matrix', layout=layout)
    while True:
        event, values=window.read()
        if event==sg.WIN_CLOSED:
            break
        elif event=='Proceed directly to application of machine learning algorithms':
            if values['_SENSORNAME_'] is '':
                sg.popup_error('Sensor name field is empty')
                continue
            window.close()
            return (dm, values['_SENSORNAME_'])
        elif event=='Data matrix action dashboard':
            if values['_SENSORNAME_'] is '':
                sg.popup_error('Sensor name field is empty')
                continue
            window.close()
            dm=options(dm, 0, 1)
            return (dm, values['_SENSORNAME_']) 
    window.close()
    return

def t2(dm):
    features=['Response(in %)','Recovery Slope', 'Response Slope', 'Recovery Time', 'Response Time', 'Integral Area', 'Ratio']
    layout1=[
    [sg.Text('Choose the feature which has been tabulated in your uploaded Type II data matrix')],
    [sg.Combo(values=features, default_value=features[0], key='_FEATURE_', size=(30, 6), readonly=True)],
    [sg.Button('Proceed directly to application of machine learning algorithms')]]
    
    layout=[[sg.Frame('MVA parameters(Mandatory)', layout=layout1)],
    [sg.Text('Press data matrix dashboard to insert columns, change indexing, visualize plots and then proceed to the ML algorithm applications', size=(50,2))],
    [sg.Button('Data matrix action dashboard')]]


    window=sg.Window('Type II matrix', layout=layout)

    while True:
        event, values=window.read()
        if event==sg.WIN_CLOSED:
            break
        elif event=='Proceed directly to application of machine learning algorithms':
            window.close()
            return (dm, values['_FEATURE_'])
        elif event=='Data matrix action dashboard':
            dm=options(dm, 0, 2)
            return (dm, values['_FEATURE_'])
    window.close()
    return


"""


