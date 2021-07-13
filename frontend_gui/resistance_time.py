import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator,FormatStrFormatter,MaxNLocator
import PySimpleGUI as sg
from frontend_gui.plotting_utils import draw_figure, draw_figure_w_toolbar, Toolbar
from frontend_gui.saving_plot import save_plot_dashboard

"""
Seeks to plot the resistance vs time curve. This function is the first step and plots all the data against the index or timestamp based on availability
"""
def response(df, t_col_no, dat_col):
    t_col=[] ##This will hold the x-axis column for plotting against
    if t_col_no is 'X' or t_col_no is 'x' or t_col_no is '':
        t_col=df.index.values.tolist()
    else:
        t_col=df.iloc[:,(int(t_col_no)-1)]


    """Figure creation using matplotlib"""
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['ps.fonttype'] = 42 ##necessary for IEEE standard PDF type publications
    mpl.rcParams['font.family'] = 'Arial' ##Recommended for publications

    fig = plt.figure(figsize=(8,4))
    ax = fig.add_subplot(111)
    for i in range((int(dat_col)-1),  df.shape[1]):
        ax.plot(t_col, df.iloc[:,i], linewidth=0.8)  ##reduction of linewidth to see the noise more clearly
    ax.xaxis.set_major_locator(plt.MaxNLocator(3))
    ax.set_title('Response Curve', fontweight='bold')
    ax.set_xlabel('Scan', fontweight ='bold')
    ax.set_ylabel('Resistance', fontweight='bold')
    ax.legend(df.columns[(int(dat_col)-1): df.shape[1]], loc='best', prop={'size': 6})




    layout = [[sg.Text('Plot of Scan vs Resistance')],
              [sg.Canvas(key='-CANVAS-', 
                         size=(600,300),
                         pad=(15,15))],
              [sg.Button('Proceed to Feature Extraction'), sg.Button('Save Plot')],
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

    
    #event loop designed in a way to allow the user to keep seeing the original plot till satisfied
    while True:
        event, values = window.read()
        if event is sg.WIN_CLOSED:
            break
        if event is 'Proceed to Feature Extraction':            
            return
        if event is 'Save Plot':
            save_plot_dashboard(fig)
        if event is 'New Plot':
            customized_plotting_dashboard(df, t_col_no, dat_col)



    window.close()


"""
This function plots the response curve using parameters from a dashboard function. Lots of parameters are left upto the user.
"""
def preview_plot(df, width, height, title, xlabel, ylabel, legend, max_x_ticks, max_y_ticks, x_col, y_col):
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
              [sg.Text('Press exit preview to go back to the plotting dashboard. Press save to choose parameters for saving image'), sg.Button('Exit Preview'), sg.Button('Save')]]


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
        if event is 'Exit Preview':            
            break
        if event is 'Save':
            save_plot_dashboard(fig)
            window.close()
            return



    window.close()

"""
Extremely useful plotting dashboard. Extreme control with the user. Default values are a good guide to understand the parameters.
The preview function allows the user to keep plotting till satisfied. The structure of this code is highly reusable for further functions.
"""
def customized_plotting_dashboard(df, t_col_no, dat_col): ##function to create plot with specific columns
    layout1=[
    [sg.Text('Enter the title of the plot', size=(45,1)), sg.Input(default_text='Response Curve', key='_TITLE_', enable_events=True)],
    [sg.Text('Enter the width of the plot (in inches)', size=(45,1)), sg.Input(default_text='8', key='_WIDTH_', enable_events=True)],
    [sg.Text('Enter the height of the plot (in inches)', size=(45,1)), sg.Input(default_text='5', key='_HEIGHT_', enable_events=True)],
    [sg.Text('Enter the x-axis label of the plot', size=(45,1)), sg.Input(default_text='Scan', key='_XLABEL_', enable_events=True)],
    [sg.Text('Enter the y-axis label of the plot', size=(45,1)), sg.Input(default_text='Resistance',key='_YLABEL_', enable_events=True)],
    [sg.Text('Enter the desired number of ticks in the x-axis', size=(45,1)), sg.Input(default_text='3', key='_XTICKS_', enable_events=True)],
    [sg.Text('Enter the desired number of ticks in the y-axis', size=(45,1)), sg.Input(default_text='3', key='_YTICKS_', enable_events=True)],
    [sg.Text('Do you require a legend in the plot?', size=(45,1)), sg.Radio('Yes', "legend", default=True, key='_LEGEND_'), sg.Radio('No', "legend", default=False)],
    [sg.Text('The pdf.fonttype used is type no 42 keeping in line with IEEE standards', size=(55,1))]]
    
    #this block is to determine the x-axis and still leave functionality to the user without a fuss. 
    #The reasoning for the default_values list having a comma on line 160 and 167 is that the list expects greater than one value and doesn't work with just one entry.
    if t_col_no is 'X' or t_col_no is 'x' or t_col_no is '':
        layout2=[
        [sg.Text('Choose the X-axis columns. You can choose the timestamp column if available or the index column', size=(45,1))],
        [sg.Combo(values=['Index',], default_value='Index', key='_XAXIS_', size=(30, 1))]]
        t_col=df.index.values.tolist()
    else:
        t_col=df.iloc[:,(int(t_col_no)-1)]
        x_cols=['Index', df.columns[(int(t_col_no)-1)]] 
        layout2=[
        [sg.Text('Choose the X-axis columns. You can choose the timestamp column if available or the index column', size=(45,1))],
        [sg.Combo(values=x_cols, default_value='Index', key='_XAXIS_', size=(30, 2))]]
         
    
    
    y_cols=df.columns[(int(dat_col)-1): df.shape[1]].tolist()
    
    layout3=[
    [sg.Text('Choose the Y-axis columns to be plotted. Multiple columns can be chosen', size=(45,1))],
    [sg.Listbox(values=y_cols, default_values=y_cols, select_mode='multiple', key='_DATA_', size=(30, 6))],
    [sg.Text('Black means selected and white means not selected')]]

    layout=[
    [sg.Frame('Plot Parameters', layout=layout1)],
    [sg.Frame('X-axis columns', layout=layout2), sg.Frame('Y-axis columns', layout=layout3)],
    [sg.Text('Click preview to view the created plot and click exit to go back to the original program', size=(45,2))],
    [sg.Button('Preview'), sg.Button('Exit')]]

    window=sg.Window('Plotting dashborad', layout=layout, size=(800,600))

    while True:
        event, v = window.Read()
        if event==sg.WIN_CLOSED or event=='Exit':
            break
        if event=='Preview':
            if v['_XAXIS_'] is 'Index':
                t_col=df.index.values.tolist()
            else:
                t_col=df.iloc[:,(int(t_col_no)-1)]
            if v['_DATA_'][0] is None:
                sg.popup_error('At least one y-axis column must be selected')
                continue

                        
            preview_plot(df, v['_WIDTH_'], v['_HEIGHT_'], v['_TITLE_'], 
                v['_XLABEL_'], v['_YLABEL_'], v['_LEGEND_'], 
                v['_XTICKS_'], v['_YTICKS_'], t_col, v['_DATA_'])

            break

    window.close()
    return











if __name__ == '__main__':
  response()
    