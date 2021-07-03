import matplotlib.pyplot as plt
import matplotlib.figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
from frontend_gui.utils import draw_figure
from frontend_gui.saving_plot import save_plot_dashboard



def response(df, t_col_no):
    t_col=[]
    if t_col_no is 'X' or t_col_no is 'x' or t_col is '':
        t_col=df.index.values.tolist()
    else:
        t_col=df.iloc[:,(int(t_col_no)-1)]
    fig = plt.figure(figsize=(6,4), dpi=100)
    plt.plot(df.iloc[:,0], df.iloc[:,1])
    plt.plot(df.iloc[:,0], df.iloc[:,2])
    


    layout = [[sg.Text('Plot of {} vs. {}'.format(df.columns[0], df.columns[1]))],
              [sg.Canvas(key='-CANVAS-', 
                         size=(700,500),
                         pad=(15,15))],
              [sg.Text('Press ok to view the next dashboard. Press save to choose parameters')],
              [sg.Button('Ok'), sg.Button('Save')]]





    # create the form and show it without the plot
    window = sg.Window('Plot', 
                       layout,
                       size=(800,600),
                       finalize=True, 
                       element_justification='center', 
                       font='Helvetica 18')

    # add the plot to the window
    fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)

    

    while True:
        event, values = window.read()
        if event is sg.WIN_CLOSED:
            break
        if event is 'Ok':            
            return
        if event is 'Save':
            save_plot_dashboard(fig)



    window.close()

if __name__ == '__main__':
  response()
    