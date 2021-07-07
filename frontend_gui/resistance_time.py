import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator,FormatStrFormatter,MaxNLocator
import PySimpleGUI as sg
from frontend_gui.plotting_utils import draw_figure, draw_figure_w_toolbar, Toolbar
from frontend_gui.saving_plot import save_plot_dashboard


def response(df, t_col_no, dat_col):
    t_col=[]
    if t_col_no is 'X' or t_col_no is 'x' or t_col is '':
        t_col=df.index.values.tolist()
    else:
        t_col=df.iloc[:,(int(t_col_no)-1)]


    """Figure creation using matplotlib"""
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['ps.fonttype'] = 42
    mpl.rcParams['font.family'] = 'Arial'

    fig = plt.figure(figsize=(10,6))
    ax = fig.add_axes([0.05,0.05,1,1])
    for i in range((int(dat_col)-1),  df.shape[1]):
        ax.plot(t_col, df.iloc[:,i])
    ax.xaxis.set_major_locator(plt.MaxNLocator(3))
    ax.set_xlabel('Scan', fontweight ='bold')
    ax.set_ylabel('Resistance', fontweight='bold')
    ax.legend(df.columns[(int(dat_col)-1): df.shape[1]], loc='best', prop={'size': 6})




    layout = [[sg.Text('Plot of {} vs. {}'.format(df.columns[0], df.columns[1]))],
              [sg.Canvas(key='-CANVAS-', 
                         size=(600,400),
                         pad=(15,15))],
              [sg.Text('Press ok to view the next dashboard. Press save to choose parameters for saving image'), sg.Button('Ok'), sg.Button('Save')],
              ]





    # create the form and show it without the plot
    window = sg.Window('Plot', 
                       layout,
                       size=(1200,800),
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

def create_plot_only(df, t_col_no, dat_col, width, height):
    fig_size=()
    fig_size=(float(width), float(height))
    t_col=[]
    if t_col_no is 'X' or t_col_no is 'x' or t_col is '':
        t_col=df.index.values.tolist()
    else:
        t_col=df.iloc[:,(int(t_col_no)-1)]


    """Figure creation using matplotlib"""
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['ps.fonttype'] = 42
    mpl.rcParams['font.family'] = 'Arial'

    fig = plt.figure(figsize=fig_size)
    ax = fig.add_axes([0.1,0.1,1,1])
    for i in range((int(dat_col)-1),  (df.shape[0]+1)):
        ax.plot(x=t_col, y=i)
    ax.xaxis.set_major_locator(plt.MaxNLocator(3))
    ax.set_xlabel('Scan', fontweight ='bold')
    ax.set_ylabel('Resistance', fontweight='bold')
    ax.legend()
    return fig




if __name__ == '__main__':
  response()
    