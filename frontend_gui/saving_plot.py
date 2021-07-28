import PySimpleGUI as sg
from frontend_gui.saving_utils import savetiff, savepng, savejpeg, savepdf, savesvg


"""
The commented out code is an alternative method which was abandoned due to ambiguity with the button functioning.
Howver, any future author is free to try the alternative layout.
"""
def save_plot_dashboard(fig):
    #file_nm_layout = [
    #[sg.Text('Enter the name of the figure in the file-browsing window which opens on clicking "Save As". Do not add any extensions', size=(50,3))],
    #[sg.InputText(key='File to Save', default_text='filename', enable_events=True),
    #sg.InputText(key='Save As', do_not_clear=False, enable_events=True, visible=False),
    #sg.FileSaveAs(initial_folder='/tmp')]]

    try:
        dirname = sg.popup_get_folder('Please choose a folder to save the plots') ##extremely useful element in pysimplegui
    except TypeError:
        return
    ##more formats can be added based on the user's requirements
    combolayout=[[sg.Combo(['PNG', 'JPEG', 'SVG', 'TIFF', 'PDF'], default_value='PNG', readonly=True, key='-LB-')]] 

    
    layout=[[sg.Text('Enter the filename', size=(45,1)), sg.Input(default_text='figure', key='_FN_', enable_events=True)],
    [sg.Text('Enter dots per inch(DPI)', size=(45,1)), sg.Input(default_text='150', key='_DPI_', enable_events=True)],   ##DPI extremely necessary
    [sg.Frame('Choose format', layout=combolayout)],
    [sg.Text('Click "Save" to save the plot and "Exit" to quit the plot saving dashboard', size=(55,1))],
    [sg.Button('Save'), sg.Button('Exit')]]

    window=sg.Window('Save plot', layout=layout, size=(800,300))##figure out if we can make multiple file saves work or just go for single save and then returning to the original plot


    while True:
        event, values = window.Read()
        if event==sg.WIN_CLOSED or event=='Exit':
            break
        if event == 'Save':
            if values['_FN_'] is '':
                sg.popup_error('Filename field empty')
                continue
            if values['_DPI_'] is '':
                sg.popup_error('DPI field empty')
                continue
            if values['-LB-']=='PNG':
                savepng(fig, dirname, values['_FN_'], values['_DPI_'])
                break
            elif values['-LB-']=='JPEG':
                savejpeg(fig, dirname, values['_FN_'], values['_DPI_'])
                break
            elif values['-LB-']=='SVG':
                savesvg(fig, dirname, values['_FN_'], values['_DPI_'])
                break
            elif values['-LB-']=='TIFF':
                savetiff(fig, dirname, values['_FN_'], values['_DPI_'])
                break
            elif values['-LB-']=='PDF':
                savepdf(fig, dirname, values['_FN_'], values['_DPI_'])
                break
            


    window.close()
    return

