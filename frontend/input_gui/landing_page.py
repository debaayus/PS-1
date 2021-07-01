import PySimpleGUI as sg

def landing_page():
    layout = [[sg.Text('Hello World')],
              [sg.Text('Press the browse button to attach .CSV or .XLSX file')],
              [sg.Button('Browse'), sg.Button('Exit')]]
    return sg.Window('Welcome', layout, finalize=True, resizable=False, size=(800,600))

    
if __name__ == '__main__':
    landing_page()              


