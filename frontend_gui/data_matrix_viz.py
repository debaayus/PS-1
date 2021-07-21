import PySimpleGUI as sg
import pandas as pd 
import numpy as np
from tkinter.font import Font
from frontend_gui.saving_data import save_data_dash
from backend import feature_extraction
from frontend_gui.plotting import conc_feature_plot_dash
"""
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

"""

def options(dm, flag, typemat):
    dm=dm.reset_index()
    header_list = list(dm.columns)
    data = dm[0:].values.tolist()
    dm=dm.set_index(dm.columns[0])

    font_family, font_size = font = ('Helvetica', 10)
    sg.set_options(font=font)
    
    table_layout=[
    [sg.Table(values=data, headings=header_list,
        enable_events=False, key='_TABLE_', 
        auto_size_columns=False,  justification='left',    
        hide_vertical_scroll=False, vertical_scroll_only=False, display_row_numbers=False
    )],
    [sg.Button('Save data matrix')]]
    
    index_change_layout = [
    [sg.Text('Enter the analyte/gas index separated by commas in a sequence. Expected number of arguments are {}'.format(dm.shape[0]), size=(50,2)), sg.Input(key='_NEWIND_', enable_events=True)],
    [sg.Text('Press submit to view the modified matrix with the new index'), sg.Button('Submit new index')]]

    column_add_layout=[[sg.Text('Add concentration column details, otherwise not present in initial data', size=(85,2))],
    [sg.Text('Enter the name of the column to be inserted', size=(50,1)), sg.Input(key='_COL_', enable_events=True)],
    [sg.Text('Enter the new values in sequence separated by commas. The number of values entered must match the number of rows in your data matrix. Expected number of entries are {}'.format(dm.shape[0]), size=(50,4)), sg.Input(key='_VAL_', enable_events=True)],
    [sg.Text('Press submit to view the modified matrix with the new column'), sg.Button('Submit new column')]]


    next_step_layout=[[sg.Text('Choose one of these options for the next dashboard')],
    [sg.Text('Press this button to go to the Feature plotting Dashboard', size=(60,1)), sg.Button('Feature Plotting Dashboard')],
    [sg.Text('This will skip the plotting dashboard and directly move to the Machine Learning module', size=(60,1)),sg.Button('ML algorithm application Dashboard')]]
        



    if flag==1:
        if typemat==1:
            layout=[[sg.TabGroup([[sg.Tab('Current Data matrix', layout=table_layout, key='table')] ,[sg.Tab('Change of index column', layout=index_change_layout, key='indchange')], 
            [sg.Tab('Add column/concentration data', layout=column_add_layout, key='add')], [sg.Tab('Next', layout=next_step_layout, key='next')]], key='tabgroup', enable_events=True)],
            [sg.Text('', size=(80,3))],
            [sg.Text('Press Reset to clear the current data matrix and go back to the feature extraction dashboard'), sg.Button('Reset')]]
            title='Type I Data matrix dashboard'
        elif typemat==2:
            layout=[[sg.TabGroup([[sg.Tab('Current Data matrix', layout=table_layout, key='table')] ,[sg.Tab('Change of index column', layout=index_change_layout, key='indchange')], 
            [sg.Tab('Add column/concentration data', layout=column_add_layout, key='add')], [sg.Tab('Next', layout=next_step_layout, key='next')]], key='tabgroup', enable_events=True)],
            [sg.Text('', size=(80,3))],
            [sg.Text('Press Reset to clear the current data matrix and go back to the feature extraction dashboard'), sg.Button('Reset')]]
            title='Type II Data matrix dashboard'
    elif flag==0:
        if typemat==1:
            layout=[[sg.TabGroup([[sg.Tab('Current Data matrix', layout=table_layout, key='table')] ,[sg.Tab('Change of index column', layout=index_change_layout, key='indchange')], 
            [sg.Tab('Add column/concentration data', layout=column_add_layout, key='add')], [sg.Tab('Next', layout=next_step_layout, key='next')]], key='tabgroup', enable_events=True)]]
            title='Type I Data matrix dashboard'
        elif typemat==2:
            layout=[[sg.TabGroup([[sg.Tab('Current Data matrix', layout=table_layout, key='table')] ,[sg.Tab('Change of index column', layout=index_change_layout, key='indchange')], 
            [sg.Tab('Add column/concentration data', layout=column_add_layout, key='add')], [sg.Tab('Next', layout=next_step_layout, key='next')]], key='tabgroup', enable_events=True)]]
            title='Type I Data matrix dashboard'
   
    window = sg.Window(title, layout=layout, grab_anywhere=False, finalize=True, size=(800,600))
    window['tabgroup'].Widget.select(0)


    while True:
        event, values= window.read()
        if event==sg.WIN_CLOSED:
            window.close()
            break
        
        if event=='Save data matrix':
            save_data_dash(dm)
            continue

        elif event=='Submit new index':
            if values['_NEWIND_'] is '':
                sg.popup_error('Index column field is empty')
                continue
            new_index=np.array([x.strip() for x in values['_NEWIND_'].split(',')])
            if len(new_index) != dm.shape[0]:
                sg.popup_error("Number of arguments does not match the shape of the data matrix")
                continue
            dm=dm.reset_index()
            dm=dm.drop(dm.columns[0], axis=1)
            dm=dm.set_index(new_index, "index")
            window.close()
            dm=options(dm, flag, typemat)
            return dm

        elif event=='ML algorithm application Dashboard':
            window.close()
            return dm

        elif event=='Feature Plotting Dashboard':
                if typemat==1:
                        conc_feature_plot_dash(dm, 1)
                    
                else:
                        conc_feature_plot_dash(dm, 2)
        elif event=='Submit new column':
            conc1= [x.strip() for x in values['_VAL_'].split(',')]
            conc=[float(i) for i in conc1]
            if len(conc) != dm.shape[0]:
                sg.popup_error("Number of arguments does not match the shape of the data matrix")
                continue
            else:
                dm.insert(0, values['_COL_'], conc)
                window.close()
                dm=options(dm, flag, typemat)
                return dm
        elif event=='Reset':
            window.close()
            return 1
    return dm





"""

    if flag==0:
        layout = [[sg.Button('View current data matrix')], [sg.Button('Change index column')], [sg.Button('Confirm data matrix for application of ML algorithms')], [sg.Button('Add concentration data')], [sg.Button('Concentration Plotting Dashboard')]]
    elif flag==1:
        layout = [[sg.Button('View current data matrix')], [sg.Button('Change index column')], [sg.Button('Confirm data matrix for application of ML algorithms')], [sg.Button('Add concentration data')], [sg.Button('Concentration Plotting Dashboard')], [sg.Button('Reset and create new data matrix')]]
    
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
            dm=pd.DataFrame()
            return dm

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
        auto_size_columns=False,  justification='left',    
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


"""

def data_matrix_landing(df, dat_col, header_list, data, ty, dm):
    ##Explain what is type 1 matrix and what is type 2 matrix. Try embedding a picture for reference
    ##Integrate landing page and dm_type() for better looks. Use data_matrix landing page to ask for poi input/ or whatever automation.
    ##Option 1: ## call backend feature extraction method. (Figure this out)
                ## Create and show data matrix using above method
                ## If user is satisfied return the created data matrix to final.py
                ## If user wants to change matrix, call this landing page again and restart process.(These buttons in table method)
    features=['Response(in %)','Recovery Slope', 'Response Slope', 'Recovery Time', 'Response Time', 'Integral Area', 'Ratio']
    
    ##table display tab
    font_family, font_size = font = ('Helvetica', 10)
    sg.set_options(font=font)
    df=df.reset_index()
    header_list_final = list(df.columns)
    data_final = df[0:].values.tolist()
    df=df.set_index(df.columns[0])
    
    frm_input_layout = [
    [sg.Table(values=data_final, headings=header_list_final,
        enable_events=False, key='_TABLE_', 
        auto_size_columns=True,  justification='left',    
        hide_vertical_scroll=False, vertical_scroll_only=False, display_row_numbers=False, size=(100, 20)
    )]]

    ###

    
    explainertab=[[sg.Text('Type I(All Features One Sensor): All the features are extracted for a single chosen sensor (based on the points of injection provided)')],
    [sg.Text('Type II(One Feature All Sensors): One chosen feature is extracted for multiple sensors (based on the points of injection provided)')],
    [sg.Text('', size=(80,3))],
    [sg.Text('The following are the features available in the extraction module', size=(80,1))],
    [sg.Multiline("1. Response% : Differential signal normalised with respect to baseline.\n2. Response slope: Maximum rate of change of signal during response.\n3. Recovery slope: Maximum rate of change of signal during recovery.\n4. Response time: The time required for 90 %% response of sensor signal in seconds.\n5. Recovery time: The time taken for 90 %% recovery of sensor signal in seconds.\n6. Integral area: Area of the signal swept between between the times of point of injection and user defined value in seconds.", disabled=True, size=(80, 8))]]

    flag=1

    parameters=[[sg.Text('Enter the points of injection(integers; no. of entries correspond to the number of signals) based on the index column of your response data. The points of injection must be separated by commas', size=(50,3)), sg.Input(key='_POI_', enable_events=True)]
    ]



    y_cols=df.columns[(int(dat_col)-1): df.shape[1]].tolist()
    layout1_type1=[[sg.Text('Choose the sensor for which the data matrix needs to be created')],
    [sg.Combo(values=y_cols, default_value=y_cols[0], key='_SENSOR_', size=(30, 6), readonly=True)],
    [sg.Text('Enter the number of seconds to calculate the integral area', size=(50,1)), sg.Input(key='_TIMETYPE1_', enable_events=True)]]
    

    layout2_type1=[[sg.Text('These are the features which will be extracted from the response data:', size=(50,1))]]
    for val in features:
        lay=[sg.Text('{}'.format(val))]
        layout2_type1.append(lay)

    layout_type1=[[sg.Frame('Sensor', layout=layout1_type1)],
    [sg.Frame('Features', layout=layout2_type1)],
    [sg.Text('Please go to the data matrix tab once you press compute')],
    [sg.Button('Compute Type I data matrix')]]


    layout1_type2=[[sg.Text('Choose the feature for which the data matrix needs to be created')],
    [sg.Combo(values=features, default_value=features[0], key='_FEATURE_', size=(30, 6), readonly=True)],
    [sg.Text('Enter the number of sensors in your array. Please do not include empty columns in your count', size=(50,2)), sg.Input(key='_TOTALSENSORS_', enable_events=True)]]

    lay2=''
    for val in y_cols:
        lay2=lay2+' '+val

    layout2_type2=[[sg.Text('The chosen feature will be extracted for all signals(based on the POI) for all sensors in the array', size=(50,1))],
    [sg.Text('These are the sensors which will be used for the feature matrix:')],
    [sg.Text(lay2, size=(85,3))]]
    
        


    layout_type2=[[sg.Frame('Feature', layout=layout1_type2)],
    [sg.Frame('Sensors', layout=layout2_type2)],
    [sg.Text('Please go to the data matrix tab once you press compute')],
    [sg.Button('Compute Type II data matrix')]]



    layout=[[sg.TabGroup([[sg.Tab('Explainer Tab', layout=explainertab, key='explainer')], [sg.Tab('Response data', layout=frm_input_layout, key='response')], [sg.Tab('Basic Input', layout=parameters, key='param')], 
        [sg.Tab('Type I matrix computation', layout=layout_type1, key='type1param')], [sg.Tab('Type II matrix computation', layout=layout_type2, key='type2 param')] ], key='tabgroup', enable_events=True)]]

    
    window = sg.Window("Feature Extraction and Data Matrix creation", auto_size_text=True, auto_size_buttons=True,
                   grab_anywhere=True, resizable=False,
                   layout=layout, finalize=True,size=(1000, 600))

    window['tabgroup'].Widget.select(0)

    ### table helper method
    window.TKroot.update()
    tree = window['_TABLE_'].Widget
    tkfont = Font(family=font_family, size=font_size)
    data_array = np.array([header_list_final]+data_final)
    
    column_widths = [max(map(lambda item:tkfont.measure(item), data_array[:, i]))
    for i in range(data_array.shape[1])]

    for heading, width in zip(header_list_final, column_widths):
        tree.column(heading, width=width+font_size+20)

    ####
    

    
    
    while True:
        event, values=window.Read()
        if event==sg.WIN_CLOSED:
            window.close()
            break
        if event=='Compute Type I data matrix':
            if values['_POI_'] is '':
                sg.popup_error('POI field is empty. Please fill the mandatory parameter')
                continue
            
            poi_string_list=[x.strip() for x in values['_POI_'].split(',')]
            poi_list=[int(i) for i in poi_string_list]
            gap=1

            if values['_TIMETYPE1_'] is '':
                sg.popup_error('Integral Area parameter empty')
                continue
            try:
                dm=feature_extraction.matrix_type1(df, poi_list, gap, int(values['_TIMETYPE1_']), values['_SENSOR_'])
            except TypeError:
                continue
            ty=1
            window.close()
            
            dm=options(dm, flag, 1)
            
            return dm
            

        elif event=='Compute Type II data matrix':
            if values['_POI_'] is '':
                sg.popup_error('POI field is empty. Please fill the mandatory parameter')
                continue
            
            poi_string_list=[x.strip() for x in values['_POI_'].split(',')]
            poi_list=[int(i) for i in poi_string_list]
            gap=1
            
            if values['_TOTALSENSORS_'] is '':
                sg.popup_error('Total number of sensors field is empty')
                continue

            if values['_FEATURE_']=='Integral Area':
                try: 
                    timeintegral=int(sg.popup_get_text('Since you have chosen integral area, please enter the number of seconds to calculate the integral area'))
                except TypeError:
                    continue
                if timeintegral is '':
                    sg.popup_error('Empty field received')
                    continue
                dm=feature_extraction.matrix_type2(values['_FEATURE_'], df, poi_list, gap, int(values['_TOTALSENSORS_']), dat_col, timeintegral)

            else:
                try: 
                    dm=feature_extraction.matrix_type2(values['_FEATURE_'], df, poi_list, gap, int(values['_TOTALSENSORS_']), dat_col, 0)
                except TypeError:
                    continue
            ##error catching needed here
            
            ty=2
            window.close()
            dm=options(dm, flag, 2)
            return dm



    return dm

