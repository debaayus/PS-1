import PySimpleGUI as sg

def save_plot_dashboard(fig):
	file_nm_layout = [
	[sg.Text('Enter the name of the figure in the file-browsing window which opens on clicking "Save As". Do not add any extensions', size=(50,3))],
	[sg.InputText(key='File to Save', default_text='filename', enable_events=True),
	sg.InputText(key='Save As', do_not_clear=False, enable_events=True, visible=False),
	sg.FileSaveAs(initial_folder='/tmp')]]

	save_png_layout=[[sg.Text('Enter dots per inch'), sg.Input(key='_png_', enable_events=True)], 
	[sg.Button('Save as PNG')]]

	save_jpeg_layout=[[]]

	save_tiff_layout=[[]]

	save_pdf_layout=[[]]


	
	layout=[[sg.Frame('Necessary parameters', layout=file_nm_layout)], 
	[sg.Frame('PNG', layout=save_png_layout)],
	[sg.Frame('JPEG', layout=save_jpeg_layout)],
	[sg.Frame('TIFF', layout=save_tiff_layout)],
	[sg.Frame('PDF', layout=save_pdf_layout)]]

	window=sg.Window('Save plot', layout=layout)

	while True:
		event, values = window.Read()
		print("event:", event, "values: ",values)
		if event==sg.WIN_CLOSED:
			break
		elif event == 'Save As':
			filename = values['Save As']
			if filename:
				window['File to Save'].update(value=filename)
			if event =='Save as PNG':
				savepng(fig, filename, values['_png_'])


	window.close()

if __name__=='__main__':
	from saving_utils import savetiff
	from saving_utils import savepng
	from saving_utils import savejpeg
	save_plot_dashboard(fig)
else:
	from frontend_gui.saving_utils import savetiff
	from frontend_gui.saving_utils import savepng
	from frontend_gui.saving_utils import savejpeg
