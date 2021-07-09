from frontend_gui import in_dat
from frontend_gui import resistance_time


def foo():
	df, data_final, header_list_final, fn, t_col_no, dat_col= in_dat.data_input()
	resistance_time.response(df, t_col_no, dat_col)

	




if __name__=='__main__':
	foo()