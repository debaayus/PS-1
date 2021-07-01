from frontend_gui import data_input
from frontend_gui.input_gui import *

def foo():
	dff, data_finall, header_list_finall, fnn= data_input.data_input() 
	print(dff.head())



if __name__=='__main__':
	foo()