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
    if t_col_no is 'X' or t_col_no is 'x' or t_col_no is '':
        t_col=df.index.values.tolist()
    else:
        t_col=df.iloc[:,(int(t_col_no)-1)]


    """Figure creation using matplotlib"""
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['ps.fonttype'] = 42
    mpl.rcParams['font.family'] = 'Arial'

    fig = plt.figure(figsize=(8,4))
    ax = fig.add_subplot(111)
    for i in range((int(dat_col)-1),  df.shape[1]):
        ax.plot(t_col, df.iloc[:,i], linewidth=0.8)
    ax.xaxis.set_major_locator(plt.MaxNLocator(3))
    ax.set_title('Response Curve', fontweight='bold')
    ax.set_xlabel('Scan', fontweight ='bold')
    ax.set_ylabel('Resistance', fontweight='bold')
    ax.legend(df.columns[(int(dat_col)-1): df.shape[1]], loc='best', prop={'size': 6})




    layout = [[sg.Text('Plot of Scan vs Resistance')],
              [sg.Canvas(key='-CANVAS-', 
                         size=(600,300),
                         pad=(15,15))],
              [sg.Text('Press ok to view the next dashboard. Press save to choose parameters for saving image'), sg.Button('Ok'), sg.Button('Save')],
              [sg.Text('Press "New Plot" to create customized plots with your choice of columns'), sg.Button('New Plot')]]





    # create the form and show it without the plot
    window = sg.Window('Plot', 
                       layout,
                       size=(800,600),
                       finalize=True, 
                       element_justification='center', 
                       font='Helvetica 10')

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
        if event is 'New Plot':
            customized_plotting_dashboard(df, t_col_no, dat_col)



    window.close()



def preview_plot(df, width, height, title, xlabel, ylabel, legend, max_x_ticks, max_y_ticks, x_col, y_col):
##function to control size and other parameters like grid and whatnot
    fig_size=(float(width), float(height))


    """Figure creation using matplotlib"""
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['ps.fonttype'] = 42
    mpl.rcParams['font.family'] = 'Arial'

    fig = plt.figure(figsize=fig_size)
    ax = fig.add_subplot(111)
    

    for col in y_col:
        ax.plot(x_col, df.loc[:,col], linewidth=0.8)
    ax.xaxis.set_major_locator(plt.MaxNLocator(int(max_x_ticks)))
    ax.yaxis.set_major_locator(plt.MaxNLocator(int(max_y_ticks)))
    ax.set_title(title , fontweight='bold')
    ax.set_xlabel(xlabel, fontweight ='bold')
    ax.set_ylabel(ylabel, fontweight='bold')
    if legend is True:
        ax.legend(y_col, loc='best', prop={'size': 6})
    else:
        pass

    layout = [[sg.Text('Plot of Scan vs Resistance')],
              [sg.Canvas(key='-CANVAS-', 
                         size=(600,400),
                         pad=(15,15))],
              [sg.Text('Press ok to go back to the plotting dashboard. Press save to choose parameters for saving image'), sg.Button('Ok'), sg.Button('Save')]]


    window = sg.Window('Plot', 
                       layout,
                       size=(900,700),
                       finalize=True, 
                       element_justification='center', 
                       font='Helvetica 10')

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
            return



    window.close()


def customized_plotting_dashboard(df, t_col_no, dat_col): ##function to create plot with specific columns
    layout1=[
    [sg.Text('Enter the title of the plot', size=(45,1)), sg.Input(default_text='Response Curve', key='_TITLE_', enable_events=True)],
    [sg.Text('Enter the width of the plot (in inches)', size=(45,1)), sg.Input(default_text='8', key='_WIDTH_', enable_events=True)],
    [sg.Text('Enter the height of the plot (in inches)', size=(45,1)), sg.Input(default_text='5', key='_HEIGHT_', enable_events=True)],
    [sg.Text('Enter the x-axis label of the plot', size=(45,1)), sg.Input(default_text='Scan', key='_XLABEL_', enable_events=True)],
    [sg.Text('Enter the y-axis label of the plot', size=(45,1)), sg.Input(default_text='Resistance',key='_YLABEL_', enable_events=True)],
    [sg.Text('Enter the desired number of ticks in the x-axis', size=(45,1)), sg.Input(default_text='3', key='_XTICKS_', enable_events=True)],
    [sg.Text('Enter the desired number of ticks in the y-axis', size=(45,1)), sg.Input(default_text='3', key='_YTICKS_', enable_events=True)],
    [sg.Text('Does the plot need a legend', size=(45,1)), sg.Radio('Yes', "legend", default=True, key='_LEGEND_'), sg.Radio('No', "legend", default=False)],
    [sg.Text('The pdf.fonttype used is type no 42 keeping in line with IEEE standards', size=(55,1))]]
    
    if t_col_no is 'X' or t_col_no is 'x' or t_col_no is '':
        layout2=[
        [sg.Text('Choose the X-axis columns. You can choose the timestamp column if available or the index column', size=(45,1))],
        [sg.Listbox(values=['Index',], default_values=['Index',], select_mode='single', key='_XAXIS_', size=(30, 1))]]
        t_col=df.index.values.tolist()
    else:
        t_col=df.iloc[:,(int(t_col_no)-1)]
        x_cols=['Index', df.columns[(int(t_col_no)-1)]] 
        layout2=[
        [sg.Text('Choose the X-axis columns. You can choose the timestamp column if available or the index column', size=(45,1))],
        [sg.Listbox(values=x_cols, default_values=['Index',], select_mode='single', key='_XAXIS_', size=(30, 2))]]
         
    
    
    y_cols=df.columns[(int(dat_col)-1): df.shape[1]].tolist()
    
    layout3=[
    [sg.Text('Choose the Y-axis columns to be plotted. Multiple columns can be chosen', size=(45,1))],
    [sg.Listbox(values=y_cols, default_values=y_cols, select_mode='multiple', key='_DATA_', size=(30, 4))]]

    layout=[
    [sg.Frame('Plot Parameters', layout=layout1)],
    [sg.Frame('X-axis columns', layout=layout2), sg.Frame('Y-axis columns', layout=layout3)],
    [sg.Text('Click preview to view the created plot and click exit to go back to the original program', size=(45,2))],
    [sg.Button('Preview'), sg.Button('Exit')]]

    window=sg.Window('Plotting dashborad', layout=layout, size=(800,700))

    while True:
        event, v = window.Read()
        if event==sg.WIN_CLOSED or event=='Exit':
            break
        if event=='Preview':
            if v['_XAXIS_'][0] is 'Index':
                t_col=df.index.values.tolist()
            else:
                t_col=df.iloc[:,(int(t_col_no)-1)]
                        
            preview_plot(df, v['_WIDTH_'], v['_HEIGHT_'], v['_TITLE_'], 
                v['_XLABEL_'], v['_YLABEL_'], v['_LEGEND_'], v['_XTICKS_'], v['_YTICKS_'], t_col, v['_DATA_'])

    window.close()
    return











if __name__ == '__main__':
  response()
    