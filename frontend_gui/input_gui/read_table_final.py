import PySimpleGUI as sg
import pandas as pd 
import numpy as np

def read_table_final(skiprow, delim, filename):  
    if filename == '':
        sg.popup_error('Empty file. Click the error button to exit')
        return

    data_final = []
    header_list_final = []
    if skiprow is'X' or skiprow is 'x':
        skiprow=-1


    skip=int(skiprow)+1
    

    if filename is not None:
        
            fn = filename.split('/')[-1]
                                
            if delim is '': 
                try:
                    df = pd.read_csv(filename, skiprows=skip, encoding='utf-16', delimiter='\t') ##dataframe read working fine
                except:
                    try:
                        df = pd.read_csv(filename, skiprows=skip, delimiter='\t')
                    except:
                        sg.popup_error('Error reading file in the read_table_final method. Click the error button to exit')
                        return
                     
            else:
                try:
                    df = pd.read_csv(filename, skiprows=skip, delimiter=delim) 
                except:
                    try:
                        df = pd.read_csv(filename, skiprows=skip, encoding='utf-16', delimiter=delim)
                    except:
                        sg.popup_error('Error reading file in the read_table_final method. Click the error button to exit')
                        return 
            header_list_final = list(df.columns) 
            data_final = df[0:].values.tolist()
            return (df,data_final, header_list_final ,fn)



if __name__ == '__main__':
    read_table_final()