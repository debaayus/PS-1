import PySimpleGUI as sg
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator,FormatStrFormatter,MaxNLocator
from frontend_gui.plotting_utils import draw_figure, draw_figure_w_toolbar, Toolbar, delete_figure_agg
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
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    ax.set_title('Response Curve', fontweight='bold')
    ax.set_xlabel('Scan', fontweight ='bold')
    ax.set_ylabel('Resistance', fontweight='bold')
    ax.margins(0)
    ax.legend(df.columns[(int(dat_col)-1): df.shape[1]], loc='upper left', bbox_to_anchor=(1,1), prop={'size': 6})

    return fig


"""
This function plots the response curve using parameters from a dashboard function. Lots of parameters are left upto the user.
"""
def preview_plot(df, theme, width, height, lw, title, title_bold, title_size, xylabelsize, xybold, xlabel, ylabel, legend, legend_size, max_x_ticks, max_y_ticks, x_col, y_col, start, end):
    fig_size=(float(width), float(height))
   

    """Figure creation using matplotlib"""
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['ps.fonttype'] = 42
    mpl.rcParams['font.family'] = 'Arial'

    
    if title_bold is True:
        title_bold='bold'
    else:
        title_bold='regular'

    if xybold is True:
        xybold='bold'
    else:
        xybold='regular'

    fig = plt.figure(figsize=fig_size)
    plt.style.use(theme)
    ax = fig.add_subplot(111)

    if start is not False and end is not False:
        for col in y_col:
            ax.plot(x_col[start:(end+1)], df.loc[start:end, col], linewidth=0.8)
    else:
        for col in y_col:
            ax.plot(x_col, df.loc[:,col], linewidth=float(lw))
    ax.xaxis.set_major_locator(plt.MaxNLocator(int(max_x_ticks)))
    ax.yaxis.set_major_locator(plt.MaxNLocator(int(max_y_ticks)))
    ax.margins(0)
    ax.set_title(title , fontsize=int(title_size), fontweight=title_bold)
    ax.set_xlabel(xlabel, fontsize=int(xylabelsize), fontweight =xybold)
    ax.set_ylabel(ylabel, fontsize=int(xylabelsize), fontweight=xybold)
    if legend is True:
        ax.legend(y_col, loc='upper left', bbox_to_anchor=(1,1), prop={'size': int(legend_size)})
    else:
        pass
    
    return fig

"""
Extremely useful plotting dashboard. Extreme control with the user. Default values are a good guide to understand the parameters.
The preview function allows the user to keep plotting till satisfied. The structure of this code is highly reusable for further functions.
"""
def customized_plotting_dashboard(df, t_col_no, dat_col): ##function to create plot with specific columns
    layout1=[
    [sg.Text('Choose the theme of the plot'), sg.Combo(values=plt.style.available, key='_THEME_', default_value='_classic_test_patch', readonly=True, size=(30,10))],
    [sg.Text('Enter the title of the plot', size=(45,1)), sg.Input(default_text='Response Curve', key='_TITLE_', enable_events=True)],
    [sg.Text('Font size of the title', size=(20,1)), sg.Input(key='_FS_', default_text='12', enable_events=True)], 
    [sg.Text('Fontweight of title: ', size=(25,1)), sg.Radio('Bold', "fw", default=True, key='_FW_'), sg.Radio('Regular', "fw", default=False)],
    [sg.Text('Enter the width of the plot (in inches)', size=(45,1)), sg.Input(default_text='8', key='_WIDTH_', enable_events=True)],
    [sg.Text('Enter the height of the plot (in inches)', size=(45,1)), sg.Input(default_text='5', key='_HEIGHT_', enable_events=True)],
    [sg.Text('Enter the line width for the plot', size=(45,1)), sg.Input(default_text='0.8', key='_LW_', enable_events=True)],
    [sg.Text('Enter the x-axis label of the plot', size=(45,1)), sg.Input(default_text='Scan', key='_XLABEL_', enable_events=True)],
    [sg.Text('Enter the y-axis label of the plot', size=(45,1)), sg.Input(default_text='Resistance',key='_YLABEL_', enable_events=True)],
    [sg.Text('Font size of the XY labels', size=(20,1)), sg.Input(key='_FSXY_', default_text='12', enable_events=True)], 
    [sg.Text('Fontweight of XY label: ', size=(25,1)), sg.Radio('Bold', "fwxy", default=True, key='_FWXY_'), sg.Radio('Regular', "fwxy", default=False)],
    [sg.Text('Enter the desired number of ticks in the x-axis', size=(45,1)), sg.Input(default_text='3', key='_XTICKS_', enable_events=True)],
    [sg.Text('Enter the desired number of ticks in the y-axis', size=(45,1)), sg.Input(default_text='3', key='_YTICKS_', enable_events=True)],
    [sg.Text('Do you require a legend in the plot?', size=(45,1)), sg.Radio('Yes', "legend", default=True, key='_LEGEND_'), sg.Radio('No', "legend", default=False)],
    [sg.Text('Enter the font size of the legend', size=(45,1)), sg.Input(key='_LZ_', enable_events=True, default_text='6')],
    [sg.Text('The pdf.fonttype used is type no 42 keeping in line with IEEE standards', size=(55,1))]]
    
    #this block is to determine the x-axis and still leave functionality to the user without a fuss. 
    #The reasoning for the default_values list having a comma on line 160 and 167 is that the list expects greater than one value and doesn't work with just one entry.
    if t_col_no is 'X' or t_col_no is 'x' or t_col_no is '':
        layout2=[
        [sg.Text('Choose the X-axis columns. You can choose the timestamp column if available or the index column', size=(45,1))],
        [sg.Combo(values=['Index',], default_value='Index', key='_XAXIS_', size=(30, 1), readonly=True)]]
        t_col=df.index.values.tolist()
    else:
        t_col=df.iloc[:,(int(t_col_no)-1)]
        x_cols=['Index', df.columns[(int(t_col_no)-1)]] 
        layout2=[
        [sg.Text('Choose the X-axis columns. You can choose the timestamp column if available or the index column', size=(45,1))],
        [sg.Combo(values=x_cols, default_value='Index', key='_XAXIS_', size=(30, 2), readonly=True)]]
         
    
    
    y_cols=df.columns[(int(dat_col)-1): df.shape[1]].tolist()
    
    layout3=[
    [sg.Text('Choose the Y-axis columns to be plotted. Multiple columns can be chosen', size=(45,1))],
    [sg.Listbox(values=y_cols, default_values=y_cols, select_mode='multiple', key='_DATA_', size=(30, 6))],
    [sg.Text('Black means selected and white means not selected')]]

    layout4=[
    [sg.Text('If you wish to plot a particular section of the graph, e.g, from the 700th data point to the 800th data point for the chosen Y-axis columns, then fill the following parameters. Otherwise please leave it blank to allow the program to plot all the data', size=(45,6))],
    [sg.Text('Enter the start index(eg. 800)', size=(45,1)), sg.Input(key='_SINDEX_', enable_events=True)],
    [sg.Text('Enter the end index(eg. 1000)', size=(45,1)), sg.Input(key='_EINDEX_', enable_events=True)]]

    layout_main=[
    [sg.Frame('Plot Parameters', layout=layout1)]]
    layout_data=[[sg.Frame('X-axis columns', layout=layout2), sg.Frame('Y-axis columns', layout=layout3)],
    [sg.Button('Preview plot')]]
    
    layout_zoom=[[sg.Frame('Optional row indexing to examine behaviour of a signal closely', layout=layout4)],
    [sg.Button('Preview zoomed plot')]]

    layout_plot=[[sg.Canvas(size=(700, 400), key='-CANVAS-', pad=(10,10))], 
    [sg.Button('Save Plot')]]

    layout=[[sg.TabGroup([[sg.Tab('Plot parameters', layout=layout_main, key='param')], [sg.Tab('Choose data', layout=layout_data, key='data')], [sg.Tab('Plot preview', layout=layout_plot, key='plot')], [sg.Tab('Zoomed plotting', layout=layout_zoom, key='zoom')]], key='tabgroup', enable_events=True)],
    [sg.Text('Press exit to leave the response curve dashboard and move to the feature extraction module'), sg.Button('Exit')]]


    window = sg.Window('Plotting dashborad', layout=layout, grab_anywhere=False, finalize=True, size=(800,600))

    figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, response(df, t_col_no, dat_col))
    window['tabgroup'].Widget.select(2)


    while True:
        event, v = window.Read()
        if event==sg.WIN_CLOSED or event=='Exit':
            break

        elif event=='Save Plot':
            save_plot_dashboard(fig)
            continue

        elif event=='Preview plot':
            if figure_agg:
                delete_figure_agg(figure_agg)
            if v['_XAXIS_'] is 'Index':
                t_col=df.index.values.tolist()
            else:
                t_col=df.iloc[:,(int(t_col_no)-1)]
            if v['_DATA_'][0] is None:
                sg.popup_error('At least one y-axis column must be selected')
                continue
            elif v['_WIDTH_'] is '':
                sg.popup_error('Width field cannot be blank')
                continue
            elif v['_HEIGHT_'] is '':
                sg.popup_error('Height field cannot be blank')
                continue
            elif v['_XLABEL_'] is '':
                sg.popup_error('X-axis label field cannot be blank')
                continue
            elif v['_YLABEL_'] is '':
                sg.popup_error('Y-axis label field cannot be blank')
                continue
            elif v['_FS_'] is '':
                sg.popup_error('Font size of title cannot be blank')
                continue
            elif v['_LW_'] is '':
                sg.popup_error('Line width field cannot be blank')
                continue
            elif v['_FSXY_'] is '':
                sg.popup_error('XY label font size field cannot be blank')
                continue
            elif v['_LZ_'] is '':
                sg.popup_error('Legend font size field cannot be blank')
                continue
            fig=preview_plot(df, v['_THEME_'], v['_WIDTH_'], v['_HEIGHT_'], v['_LW_'], v['_TITLE_'], v['_FW_'], v['_FS_'],  
                            v['_FSXY_'], v['_FWXY_'], v['_XLABEL_'], v['_YLABEL_'], v['_LEGEND_'], v['_LZ_'],  
                            v['_XTICKS_'], v['_YTICKS_'], t_col, v['_DATA_'], False, False)
            figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
            window['tabgroup'].Widget.select(2)

        elif event=='Preview zoomed plot':
            if figure_agg:
                delete_figure_agg(figure_agg)
            if v['_XAXIS_'] is 'Index':
                t_col=df.index.values.tolist()
            else:
                t_col=df.iloc[:,(int(t_col_no)-1)]
            if v['_DATA_'][0] is None:
                sg.popup_error('At least one y-axis column must be selected')
                continue
            elif v['_WIDTH_'] is '':
                sg.popup_error('Width field cannot be blank')
                continue
            elif v['_HEIGHT_'] is '':
                sg.popup_error('Height field cannot be blank')
                continue
            elif v['_XLABEL_'] is '':
                sg.popup_error('X-axis label field cannot be blank')
                continue
            elif v['_YLABEL_'] is '':
                sg.popup_error('Y-axis label field cannot be blank')
                continue
            elif v['_FS_'] is '':
                sg.popup_error('Font size of title cannot be blank')
                continue
            elif v['_LW_'] is '':
                sg.popup_error('Line width field cannot be blank')
                continue
            elif v['_FSXY_'] is '':
                sg.popup_error('XY label font size field cannot be blank')
                continue
            elif v['_LZ_'] is '':
                sg.popup_error('Legend font size field cannot be blank')
                continue
            if v['_SINDEX_'] is '' or v['_EINDEX_'] is '':
                sg.popup_error('Either of the indexes are empty')
                continue
            fig=preview_plot(df, v['_THEME_'], v['_WIDTH_'], v['_HEIGHT_'], v['_LW_'], v['_TITLE_'], v['_FW_'], v['_FS_'],  
                            v['_FSXY_'], v['_FWXY_'], v['_XLABEL_'], v['_YLABEL_'], v['_LEGEND_'], v['_LZ_'],  
                            v['_XTICKS_'], v['_YTICKS_'], t_col, v['_DATA_'], int(v['_SINDEX_']), int(v['_EINDEX_']))
            figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
            window['tabgroup'].Widget.select(2)
            

    window.close()
    return

def conc_feature_plot_dash_type1(dm, fea_start):
    layout1=[
    [sg.Text('Enter the title of the plot', size=(45,1)), sg.Input(default_text='Concentration vs Feature Plot', key='_TITLE_', enable_events=True)],
    [sg.Text('Enter the width of the plot (in inches)', size=(45,1)), sg.Input(default_text='8', key='_WIDTH_', enable_events=True)],
    [sg.Text('Enter the height of the plot (in inches)', size=(45,1)), sg.Input(default_text='5', key='_HEIGHT_', enable_events=True)],
    [sg.Text('Enter the x-axis label of the plot', size=(45,1)), sg.Input(default_text='Concentration', key='_XLABEL_', enable_events=True)],
    [sg.Text('Enter the y-axis label of the plot', size=(45,1)), sg.Input(default_text='Feature',key='_YLABEL_', enable_events=True)],
    [sg.Text('The pdf.fonttype used is type no 42 keeping in line with IEEE standards', size=(55,1))]]

    x_cols=[]
    x_cols=dm.columns[0:fea_start].tolist()
    
    y_cols=[]
    y_cols=dm.columns[fea_start:].tolist()
    layout2=[
        [sg.Text('Choose the X-axis concentration column', size=(45,1)), sg.Combo(values=x_cols, default_value=x_cols[0], key='_XAXIS_', size=(30, 1), readonly=True)],
        [sg.Text('Choose the feature you want to plot against the concentration. Single feature can be chosen', size=(45,1)), sg.Combo(values=y_cols, default_value=y_cols[0], key='_FEATURE_', size=(30, 6), readonly=True)],
        [sg.Button('Plot Feature(Y) vs Concentration(X)')]]
    

    layout3=[
        [sg.Text('Choose the feature column as X axis. Only one feature/X-axis column can be chosen', size=(45,1)), sg.Combo(values=y_cols, default_value=y_cols[0], key='_FEATUREREV_', size=(30, 1), readonly=True)],
        [sg.Text('Choose the concentration column to be plotted in the Y axis', size=(45,1)), sg.Combo(values=x_cols, default_value=x_cols[0], key='_XAXISREV_', size=(30, 6), readonly=True)],
        [sg.Button('Plot Concentration(Y) vs Feature(X)')]]

    layout=[[sg.Frame('Basic parameters', layout=layout1)],
    [sg.Frame('X-axis: Concentration and Y-axis: Feature', layout=layout2)],
    [sg.Frame('X-axis: Feature and Y-axis: Concentration', layout=layout3)],
    [sg.Text('Labels will be created as "index-concentration"')],
    [sg.Text('Press exit to go back to the actions dashboard'), sg.Button('Exit')]]

    window=sg.Window("Type I matrix plotting dashboard", layout=layout)

    while True:
        event, v = window.Read()
        if event==sg.WIN_CLOSED or event=='Exit':
            break
        elif event=='Plot Feature(Y) vs Concentration(X)':
            conc_feature_preview_type1(dm, v['_WIDTH_'], v['_HEIGHT_'], v['_TITLE_'], v['_XLABEL_'], v['_YLABEL_'], v['_XAXIS_'], v['_FEATURE_'], 0, 0)
        elif event=='Plot Concentration(Y) vs Feature(X)':
            conc_feature_preview_type1(dm, v['_WIDTH_'], v['_HEIGHT_'], v['_TITLE_'], v['_XLABEL_'], v['_YLABEL_'], 0, 0, v['_FEATUREREV_'], v['_XAXISREV_'])
    window.close()
    return


  
    

def conc_feature_plot_dash_type2(dm, sens_start):
    layout1=[
    [sg.Text('Enter the title of the plot', size=(45,1)), sg.Input(default_text='Concentration vs Sensor Feature Plot', key='_TITLE_', enable_events=True)],
    [sg.Text('Enter the width of the plot (in inches)', size=(45,1)), sg.Input(default_text='8', key='_WIDTH_', enable_events=True)],
    [sg.Text('Enter the height of the plot (in inches)', size=(45,1)), sg.Input(default_text='5', key='_HEIGHT_', enable_events=True)],
    [sg.Text('Enter the x-axis label of the plot', size=(45,1)), sg.Input(default_text='Concentration', key='_XLABEL_', enable_events=True)],
    [sg.Text('Enter the y-axis label of the plot', size=(45,1)), sg.Input(default_text='Sensor Feature',key='_YLABEL_', enable_events=True)],
    [sg.Text('The pdf.fonttype used is type no 42 keeping in line with IEEE standards', size=(55,1))]]

    x_cols=[]
    x_cols=dm.columns[0:sens_start].tolist()
    
    y_cols=[]
    y_cols=dm.columns[sens_start:].tolist()
    layout2=[
        [sg.Text('Choose the X-axis concentration column', size=(45,1)), sg.Combo(values=x_cols, default_value=x_cols[0], key='_XAXIS_', size=(30, 1), readonly=True)],
        [sg.Text('Choose the sensors for which you want to plot the feature against the concentration Y-axis', size=(45,2)), sg.Listbox(values=y_cols, default_values=[y_cols[0],], select_mode='multiple', key='_FEATURE_', size=(30, 6))],
        [sg.Button('Plot Sensor Feature(Y) vs Concentration(X)')]]
    



    layout=[[sg.Frame('Basic parameters', layout=layout1)],
    [sg.Frame('X-axis: Concentration and Y-axis: Sensor feature', layout=layout2)],
    [sg.Text('Labels will be created by sensor names')],
    [sg.Text('Press exit to go back to the actions dashboard'), sg.Button('Exit')]]

    window=sg.Window("Type II matrix plotting dashboard", layout=layout)

    while True:
        event, v = window.Read()
        if event==sg.WIN_CLOSED or event=='Exit':
            break
        elif event=='Plot Sensor Feature(Y) vs Concentration(X)':
            conc_feature_preview_type2(dm, v['_WIDTH_'], v['_HEIGHT_'], v['_TITLE_'], v['_XLABEL_'], v['_YLABEL_'], v['_XAXIS_'], v['_FEATURE_'])
    window.close()
    return




def conc_feature_preview_type1(dm, width, height, title, xlabel, ylabel, concX, featureY, featureX, concY):
    fig_size=(float(width), float(height))


    """Figure creation using matplotlib"""
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['ps.fonttype'] = 42
    mpl.rcParams['font.family'] = 'Arial'

    fig = plt.figure(figsize=fig_size)
    ax = fig.add_subplot(111)

    if concY==0 and featureX==0:
        
        label=[]
        index_val=[str(x) for x in dm.index.values.tolist()]
        conc_val=[str(x) for x in dm.loc[:, concX].tolist()]
        label=[a + "_" + b for a, b in zip(index_val, conc_val )]
        ax.scatter(dm.loc[:, concX], dm.loc[:,featureY], alpha=0.8, s=25)
        ax.legend(labels=label, loc='upper left', bbox_to_anchor=(1,1))
        
    elif concX==0 and featureY==0:
        label=[]
        index_val=[str(x) for x in dm.index.values.tolist()]
        conc_val=[str(x) for x in dm.loc[:, concY].tolist()]
        label=[a +"_"+ b for a, b in zip(index_val, conc_val)]
        ax.scatter(dm.loc[:,featureX], dm.loc[:, concY], alpha=0.6, s=25)
        ax.legend(labels=label, loc='upper left', bbox_to_anchor=(1,1))

    


    ax.grid()
    ax.set_title(title , fontweight='bold')
    ax.set_xlabel(xlabel, fontweight ='bold')
    ax.set_ylabel(ylabel, fontweight='bold')


    layout = [[sg.Text('Plot of Concentraion and Feature')],
              [sg.Canvas(key='-CANVAS-', 
                         size=(600,400),
                         pad=(5,10))],
              [sg.Text('Press exit preview to go back to the plotting dashboard. Press save to choose parameters for saving image'), sg.Button('Exit Preview'), sg.Button('Save')]]


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
        if event is 'Exit Preview':            
            break
        if event is 'Save':
            save_plot_dashboard(fig)
            window.close()
            return



    window.close()
    return



def conc_feature_preview_type2(dm, width, height, title, xlabel, ylabel, concX, sensorsY):
    fig_size=(float(width), float(height))


    """Figure creation using matplotlib"""
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['ps.fonttype'] = 42
    mpl.rcParams['font.family'] = 'Arial'

    fig = plt.figure(figsize=fig_size)
    ax = fig.add_subplot(111)

    
    for val in sensorsY:
        ax.scatter(dm.loc[:, concX], dm.loc[:,val], label=val, alpha=0.8, s=25)
        ax.legend(loc='upper left', bbox_to_anchor=(1,1))
        

    


    ax.grid()
    ax.set_title(title , fontweight='bold')
    ax.set_xlabel(xlabel, fontweight ='bold')
    ax.set_ylabel(ylabel, fontweight='bold')


    layout = [[sg.Text('Plot of Concentraion and Sensor Feature')],
              [sg.Canvas(key='-CANVAS-', 
                         size=(600,400),
                         pad=(5,10))],
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
    return
    









if __name__ == '__main__':
  response()
    