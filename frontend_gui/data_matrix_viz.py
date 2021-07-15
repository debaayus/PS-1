import PySimpleGUI as sg
import pandas as pd 
import numpy as np
from tkinter.font import Font
from frontend_gui.saving_data import save_data_dash
from frontend_gui.plotting import conc_feature_plot_dash_type1
from frontend_gui.plotting import conc_feature_plot_dash_type2
from backend import feature_extraction


def type1(df, dat_col):
    y_cols=df.columns[(int(dat_col)-1): df.shape[1]].tolist()
    layout1=[[sg.Text('Choose the sensor for which the data matrix needs to be created')],
    [sg.Combo(values=y_cols, default_value=y_cols[0], key='_SENSOR_', size=(30, 6), readonly=True)]]
    

    layout2=[[sg.Text('These are the features which will be extracted from the response data:')],
    [sg.Text("Response(in %), Recovery Slope, Response Slope, Recovery Time, Response Time, Integral Area, Ratio")]]

    layout=[[sg.Frame('Sensor', layout=layout1)],
    [sg.Frame('Features', layout=layout2)],
    [sg.Button('Proceed to Type I data matrix computation'), sg.Cancel()]]

    window=sg.Window('Type I matrix parameters', layout=layout)

    while True:
        event, values= window.read()
        if event==sg.WIN_CLOSED or event=='Cancel':
            break
        if event=='Proceed to Type I data matrix computation':
                try:
                    timeintegral=sg.popup_get_text('Please enter the number of seconds to calculate the integral area')
                    if timeintegral is '':
                        sg.popup_error('Empty field received')
                        continue
                    else:
                        window.close()
                        return (values['_SENSOR_'], int(timeintegral))
                except TypeError:
                    continue  
    window.close()
    return

def type2(df, dat_col, features):
    layout1=[[sg.Text('Choose the feature for which the data matrix needs to be created')],
    [sg.Combo(values=features, default_value=features[0], key='_FEATURE_', size=(30, 6), readonly=True)]]

    y_cols=df.columns[(int(dat_col)-1): df.shape[1]].tolist()
    
    layout2=[[sg.Text('The chosen feature will be extracted for all signals(based on the POI) for all sensors in the array')],
    [sg.Text('{}'.format(df.columns))]]

    layout=[[sg.Frame('Feature', layout=layout1)],
    [sg.Frame('Sensors', layout=layout2)],
    [sg.Button('Proceed to data matrix Type II computation'), sg.Cancel()]]
    
    window=sg.Window('Type II matrix parameters', layout=layout)

    while True:
        event, values= window.read()
        if event==sg.WIN_CLOSED or event=='Cancel':
            break
        if event=='Proceed to data matrix Type II computation':
            if values['_FEATURE_']=='Integral Area':
                try:
                    timeintegral=sg.popup_get_text('Since you have chosen integral area, please enter the number of seconds to calculate the integral area')
                    if timeintegral is '':
                        sg.popup_error('Empty field received')
                        continue
                    else:
                        window.close()
                        return (values['_FEATURE_'], int(timeintegral))
                except TypeError:
                    continue 
            else:
                window.close()
                return (values['_FEATURE_'], 0)

    window.close()
    return

def options(dm, flag, typemat):
    if flag==0:
        layout = [[sg.Button('View current data matrix')], [sg.Button('Change index column')], [sg.Button('Confirm data matrix for application of ML algorithms')], [sg.Button('Add concentration data')], [sg.Button('Concentration Plotting Dashboard')]]
    elif flag==1:
        layout = [[sg.Button('View current data matrix')], [sg.Button('Change index column')], [sg.Button('Confirm data matrix for application of ML algorithms')], [sg.Button('Add concentration data')], [sg.Button('Reset and create new data matrix')]]
    
    window=sg.Window("Data matrix action dashboard", layout=layout)
    

    while True:
        event, values= window.read()
        if event==sg.WIN_CLOSED:
            break

        elif event=='View current data matrix':
            data_matrix_table(dm)
            continue
        elif event=='Change index column':
            user_index=sg.popup_get_text('Enter the analyte/gas index separated by commas in a sequence. Expected number of arguments are {}'.format(dm.shape[0]))
            if user_index is None:
                continue
            new_index=np.array([x.strip() for x in user_index.split(',')])
            if len(new_index) != dm.shape[0]:
                sg.popup_error("Number of arguments does not match the shape of the data matrix")
                continue
            dm=dm.reset_index()
            dm=dm.drop(dm.columns[0], axis=1)
            dm=dm.set_index(new_index, "index")
            data_matrix_table(dm)
            continue
        elif event=='Confirm data matrix for application of ML algorithms':
            window.close()
            return dm
        elif event=='Concentration Plotting Dashboard':
            prompt=sg.popup_yes_no('Does your data matrix have concentration data?')
            if prompt=='Yes':
                if typemat==1:
                    try:
                        fea_start=sg.popup_get_text('Enter the column number of the first feature column(eg. 3 for the third column). You can press cancel and press "View current data matrix" and then come back to this option', size=(40,4))
                        conc_feature_plot_dash_type1(dm, int(fea_start)-2)
                    except TypeError:
                        continue
                else:
                    try:
                        sensor_start=sg.popup_get_text('Enter the column number of the first sensor column(Minimum value=3 as index and concentration columns must preceed feature columns)You can press cancel and press "View current data matrix" and then come back to this option', size=(40,4))
                        conc_feature_plot_dash_type2(dm, int(sensor_start)-2)
                    except TypeError:
                        continue
            else:
                sg.popup_error('Please add concentration data using the dashboard')
                continue
        elif event=='Add concentration data':
            dm= conc_append(dm)
            data_matrix_table(dm)
            prompt=sg.popup_yes_no('Do you wish to plot concentration and features?')
            if prompt is 'Yes':
                if typemat==1:
                    try:
                        fea_start=sg.popup_get_text('Enter the column number of the first feature column(Minimum value=3 as index and concentration columns must preceed feature columns). You can press cancel and press "View current data matrix" and then come back to this option', size=(40,4))
                        conc_feature_plot_dash_type1(dm, int(fea_start)-2)
                    except TypeError:
                        continue
                else:
                    try:
                        sensor_start=sg.popup_get_text('Enter the column number of the first sensor column(Minimum value=3 as index and concentration columns must preceed feature columns). You can press cancel and press "View current data matrix" and then come back to this option', size=(40,4))
                        conc_feature_plot_dash_type2(dm, int(sensor_start)-2)
                    except TypeError:
                        continue
            else:
                continue
        elif event=='Reset and create new data matrix':
            window.close()
            return 0

    window.close()
    return




def data_matrix_table(dm):
    ## ask if they want to change index in the data matrix created
    dm=dm.reset_index()
    header_list = list(dm.columns)
    data = dm[0:].values.tolist()
    dm=dm.set_index(dm.columns[0])
    
    font_family, font_size = font = ('Helvetica', 10)
    sg.set_options(font=font)
    frm_table_layout = [
    [sg.Table(values=data, headings=header_list,
        enable_events=False, key='_TABLE_', 
        auto_size_columns=True,  justification='left',    
        hide_vertical_scroll=False, vertical_scroll_only=False, display_row_numbers=False
    )]]
    
    
    layout=[[sg.Frame('Input', frm_table_layout)],[sg.Text('Press OK to return to matrix actions')],[sg.Button('Save matrix in file format'), sg.Button('OK')]]


    window = sg.Window("Data matrix", auto_size_text=True, auto_size_buttons=True,
                   grab_anywhere=True, resizable=False,
                   layout=layout, finalize=True)

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
        elif event=='Save matrix in file format':
            save_data_dash(dm)
            break
        elif event=='OK':
            break

    window.close()
    return 



def conc_append(dm):
    layout= [[sg.Text('If you wish to visualize concentration and a feature in a plot, please enter the following parameters', size=(50,2))],
    [sg.Text('Enter the name of the concentration column to be inserted', size=(50,1)), sg.Input(key='_COL_', enable_events=True)],
    [sg.Text('Enter the concentration values in sequence separated by commas. The number of values entered must match the number of rows in your data matrix', size=(50,4))],
    [sg.Text('Expected number of concentration entries are {}'.format(dm.shape[0]))],
    [sg.Input(key='_CONC_', enable_events=True)],
    [sg.Button('View modified data matrix')]]

    window=sg.Window('Concentration data', layout=layout)
    while True:
        event, values=window.read()
        if event==sg.WIN_CLOSED:
            break
        if event=='View modified data matrix':
            conc1= [x.strip() for x in values['_CONC_'].split(',')]
            conc=[float(i) for i in conc1]
            if len(conc) != dm.shape[0]:
                sg.popup_error("Number of arguments does not match the shape of the data matrix")
                continue
            else:
                dm.insert(0, values['_COL_'], conc)
                return dm 
    window.close()
    return




def data_matrix_landing(df, dat_col):
    ##Explain what is type 1 matrix and what is type 2 matrix. Try embedding a picture for reference
    ##Integrate landing page and dm_type() for better looks. Use data_matrix landing page to ask for poi input/ or whatever automation.
    ##Option 1: ## call backend feature extraction method. (Figure this out)
                ## Create and show data matrix using above method
                ## If user is satisfied return the created data matrix to final.py
                ## If user wants to change matrix, call this landing page again and restart process.(These buttons in table method)
    features=['Response(in %)','Recovery Slope', 'Response Slope', 'Recovery Time', 'Response Time', 'Integral Area', 'Ratio']
    
    explainertable=[[sg.Text('Type I: This type of matrix will extract your chosen features for every signal(every injection) of a single sensor from your response data', size=(50,4))],
                    [sg.Text('Type II: This type of matrix will extract one feature for every signal(every injection) of the chosen sensors from your response data', size=(50,4))]]
    typeofmatrix=[[sg.Text('Confirm the type of matrix you want to create')], 
    [sg.Radio('Type I', "type", default=True, key='_TYPE_'),
    sg.Radio('Type II', "type", default=False)]]

    flag=1

    parameters=[[sg.Text('Enter the points of injection(integers; corresponding to the number of signals) based on the the timestamp column(not index column) of your response data. The points of injection must be separated by commas', size=(50,5)), sg.Input(key='_POI_', enable_events=True)],
    [sg.Text('Enter the gap(in seconds) between each data point. If no time reference available, please leave it blank', size=(50,2)), sg.Input(key='_GAP_', enable_events=True)],
    [sg.Text('Enter the number of sensors in your array. Please do not include empty columns in your count', size=(50,2)), sg.Input(key='_TOTALSENSORS_', enable_events=True)]]

    layout=[[sg.Frame('Explanation of the type of feature matrix', layout=explainertable)],
    [sg.Frame('Type of matrix to be created', layout=typeofmatrix)],
    [sg.Frame('Basic Parameters for feature extraction', layout=parameters)],
    [sg.Text('Press submit to proceed to adding specific details for either Type I or Type II')],
    [sg.Button('Submit')]]

    
    window=sg.Window("Feature extraction and Data Matrix creation", layout=layout)
    while True:
        event, values=window.Read()
        if event==sg.WIN_CLOSED:
            break
        if event=='Submit':
            if values['_POI_'] is '' or values['_GAP_'] is '':
                sg.popup_error('POI or Gap fields are empty. Please fill these mandatory parameters')
                continue
            poi_string_list=[x.strip() for x in values['_POI_'].split(',')]
            poi_list=[int(i) for i in poi_string_list]
            gap=int(values['_GAP_'])
            if values['_TYPE_'] is False:
                ##code for Type 2
                dm=pd.DataFrame()
                feature, time=type2(df, dat_col, features)
                dm=feature_extraction.matrix_type2(feature,df,poi_list,gap, int(values['_TOTALSENSORS_']),dat_col, time)

                ##feature extraction method which returns a data matrix with correct indexing and columns [ dm=xyz(params) ] 
                ##available parameters for type 2: poi_list(list of strings), gap(integer in seconds), sensors(list of strings)
                ##                                 time(integer; its 0 if user has not chosen integral area), feature(string),
                ##                                 type of matrix can directly be passed to the parameter list 
                
                dm=options(dm, flag, 2)
                if dm==0:
                    continue
                else:
                    window.close()
                    return dm
            elif values['_TYPE_'] is True:
                ##Code for type 1
                dm=pd.DataFrame()
                sensor, time=type1(df, dat_col)
                dm=feature_extraction.matrix_type1(df, poi_list, gap, time, sensor)
                
                ##feature extraction method which returns a data matrix with correct indexing and columns [ dm=xyz(params) ] 
                ##available parameters for type 1: poi_list(list of strings), gap(integer in seconds), sensor(string) 
                ##                                 time(integer; its 0 if user has not chosen integral area), features(list of strings),
                ##                                 type of matrix can directly be passed to the parameter list
                
                dm=options(dm, flag, 1)
                if dm==0:
                    continue
                else:
                    window.close()
                    return dm
    window.close()
    return

