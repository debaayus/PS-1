from frontend_gui import in_dat


def foo():
	dff, data_finall, header_list_finall, fnn= in_dat.data_input() 
	print(dff.head())



if __name__=='__main__':
	foo()