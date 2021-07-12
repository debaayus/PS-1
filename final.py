from frontend_gui import in_dat
from frontend_gui import resistance_time
from frontend_gui import data_matrix_viz


def foo():
    flag=0
    try:
        df, data_final, header_list_final, fn, t_col_no, dat_col= in_dat.data_input()
        flag=1
    except ValueError:
        pass

    if flag==0:
        dm, typemat, fn= in_dat.data_input()
        flag=2
        ##go to MVA directly
    

    
    elif flag==1:
        resistance_time.response(df, t_col_no, dat_col)
        while True:
            data_matrix_viz.data_matrix_landing(df, dat_col)
            ##go to data matrix viz
            ##get data matrix using backend and visualize 
            ##go to MVA and complete MVA
            ##In MVA, allow user to try different methods. Allow coming back to original MVA dashboard
            ##popup asking to create new data matrix for the same response data for new analysis
            ##if popup says no break otherwise continue.

    
    

    





if __name__=='__main__':
    foo()