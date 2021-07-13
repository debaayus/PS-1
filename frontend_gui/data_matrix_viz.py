import PySimpleGUI as sg
import pandas as pd 
import numpy as np
from tkinter.font import Font
from frontend_gui.saving_data import save_data_dash
##from backend import data matrix

def dm_type():

    layout=[[sg.Text('Select the type of feature matrix that needs to be plotted')],
    [sg.Listbox(values=['Type I', 'Type II'], default_values=['Type I',], select_mode='single', key='_TYPE_', size=(30, 3))],
    [sg.Button('Confirm'), sg.Button('Cancel')]]

    window=sg.window('Data Matrix Type', layout=layout)

    while True:
        event, values= window.read()
        if event==sg.WIN_CLOSED or event=='Cancel':
            break
        if event=='Confirm':
            window.close()
            if values['_TYPE_'][0] is 'Type I':
                return 1
            elif values['_TYPE_'][0] is 'Type II':
                return 2
    window.close()
    return

def type1(df, dat_col, features):
    y_cols=df.columns[(int(dat_col)-1): df.shape[1]].tolist()
    layout1=[[sg.Text('Choose the sensor for which the data matrix needs to be created')],
    [sg.Combo(values=y_cols, default_value=y_cols[0], key='_SENSOR_', size=(30, 6), readonly=True)]]
    

    layout2=[[sg.Text('Choose the features for your Type I data matrix. Multiple features should be chosen(preferably all)')],
    [sg.Text('Black means chosen and white means not chosen')],
    [sg.Listbox(values=features, default_values=features, select_mode='multiple', key='_FEATURES_', size=(30, 6))]]

    layout=[[sg.Frame('Sensor', layout=layout1)],
    [sg.Frame('Features', layout=layout2)],
    [sg.Button('Proceed to data matrix Type I computation'), sg.Cancel()]]

    window=sg.window('Type I matrix parameters', layout=layout)

    while True:
        event, values= window.read()
        if event==sg.WIN_CLOSED or event=='Cancel':
            break
        if event=='Proceed to data matrix Type I computation':
            window.close()
            return (values['_SENSOR_'], values['_FEATURES_'])
    window.close()
    return

def type2(df, dat_col, features):
    layout1=[[sg.Text('Choose the feature for which the data matrix needs to be created')],
    [sg.Combo(values=features, default_value=features[0], key='_FEATURE_', size=(30, 6), readonly=True)]]

    y_cols=df.columns[(int(dat_col)-1): df.shape[1]].tolist()
    
    layout2=[[sg.Text('Choose the sensors for your Type II data matrix. Multiple features should be chosen(preferably all)')],
    [sg.Text('Black means chosen and white means not chosen')],
    [sg.Listbox(values=y_cols, default_values=y_cols, select_mode='multiple', key='_SENSORS_', size=(30, 6))]]

    layout=[[sg.Frame('Feature', layout=layout1)],
    [sg.Frame('Sensors', layout=layout2)],
    [sg.Button('Proceed to data matrix Type II computation'), sg.Cancel()]]
    
    window=sg.window('Type II matrix parameters', layout=layout)

    while True:
        event, values= window.read()
        if event==sg.WIN_CLOSED or event=='Cancel':
            break
        if event=='Proceed to data matrix Type II computation':
            window.close()
            return (values['_FEATURE_'], values['_SENSORS_'])
    window.close()
    return


def data_matrix_table():
    pass    



def data_matrix_landing(df, dat_col):
    ##Explain what is type 1 matrix and what is type 2 matrix. Try embedding a picture for reference
    ##Integrate landing page and dm_type() for better looks. Use data_matrix landing page to ask for poi input/ or whatever automation.
    ##Option 1: ## call backend feature extraction method. (Figure this out)
                ## Create and show data matric using above method
                ## If user is satisfied return the created data matrix to final.py
                ## If user wants to change matrix, call this landing page again and restart process.(These buttons in table method)
    features=['Sensitivity','Recovery Slope', 'Response Slope', 'Recovery Time', 'Response Time', 'Integral Area']





if __name__ == '__main__':
	dm_dash()
	