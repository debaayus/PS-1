from frontend_gui import in_dat
from frontend_gui import resistance_time


def foo():
    flag=0
    try:
        df, data_final, header_list_final, fn, t_col_no, dat_col= in_dat.data_input()
        flag=1
    except ValueError:
        pass

    if flag==1:
        dm, typemat, fn= in_dat.data_input()
        flag=2
    

    
    if flag==1:
        resistance_time.response(df, t_col_no, dat_col)
    


    





if __name__=='__main__':
    foo()