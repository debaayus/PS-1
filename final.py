from frontend_gui import in_dat
from frontend_gui import plotting
from frontend_gui import data_matrix_viz
import PySimpleGUI as sg


"""
This is the main function which controls the event loops and program sequence for the input part of the GUI.
"""
def foo():
    flag=0
    home= in_dat.landing_page()

    while True:  # Event Loop
        event, values = home.read()

        if event == sg.WIN_CLOSED or event == 'Exit':  # if all windows were closed
            break
        elif event == 'Upload response data':
            try:
                data, header_list,fn, filename=in_dat.read_table()
                show_prompt = sg.popup_yes_no('Process the sensor response data?')
                if show_prompt=='Yes':
                    home.close()
                    skiprow, delim, filename=in_dat.show_table(data, header_list, fn, filename)
                    df, data_final, header_list_final, fn = in_dat.read_table_final(skiprow, delim, filename)
                    df, data_final, header_list_final, fn, t_col_no, dat_col = in_dat.show_table_final(df,data_final, header_list_final ,fn) #any index updates if needed
                    flag=1
                    break
                else:
                    continue
            except TypeError:
                continue
        elif event=='Upload data matrix':
            try:
                data, header_list,fn, filename=in_dat.read_table()
                show_prompt = sg.popup_yes_no('Process the feature matrix?')
                if show_prompt=='Yes':
                    home.close()
                    skiprow, delim, filename=in_dat.show_table(data, header_list, fn, filename)
                    df, data_final, header_list_final, fn = in_dat.read_table_final(skiprow, delim, filename)
                    dm, typemat, sens_name_or_feature = in_dat.show_table_MVA(df, data_final, header_list_final ,fn) 
                    flag=2
                    break
                else:
                    continue
            except TypeError:
                continue

    home.close()
    

    
    if flag==1:
        plotting.customized_plotting_dashboard(df, t_col_no, dat_col)
        dm=1
        while dm==1:            
                header_list=[]
                data=[[]]
                ty=0
                dm=[[]]
                dm=data_matrix_viz.data_matrix_landing(df, dat_col, header_list, data, ty, dm)
                try:
                    if dm==1:
                        print("triggered")
                        continue
                except ValueError:
                    break



    if flag==2:
        print(dm) 

        
        #while True:
            #data_matrix_viz.data_matrix_landing(df, dat_col)
            
            ##go to data matrix viz
            ##get data matrix using backend and visualize 
            ##go to MVA and complete MVA
            ##In MVA, allow user to try different methods. Allow coming back to original MVA dashboard
            ##popup asking to create new data matrix for the same response data for new analysis
            ##if popup says no break otherwise continue.

    
    

    





if __name__=='__main__':
    foo()