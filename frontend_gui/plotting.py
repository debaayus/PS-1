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

    fig = plt.figure(figsize=(10,6))
    ax = fig.add_subplot(111)
    for i in range((int(dat_col)-1),  df.shape[1]):
        ax.plot(t_col, df.iloc[:,i], linewidth=0.8)  ##reduction of linewidth to see the noise more clearly
    ax.set_xlim(0, max(t_col))
    ax.set_ylim(0)
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    ax.set_title('Response Curve', fontweight='bold')
    ax.set_xlabel('Scan', fontweight ='bold')
    ax.set_ylabel('Resistance', fontweight='bold')
    ax.margins(x=0)
    ax.margins(y=0.05)
    ax.legend(df.columns[(int(dat_col)-1): df.shape[1]], loc='upper left', bbox_to_anchor=(1,1), prop={'size': 6})

    return fig


"""
This function plots the response curve using parameters from a dashboard function. Lots of parameters are left upto the user.
"""
def preview_plot(df, theme, width, height, lw, title, title_bold, title_size, xylabelsize, xybold, 
    xlabel, ylabel, legend, legend_size, xticksize, yticksize, max_x_ticks, max_y_ticks, 
    xmargin, ymargin, x_col, y_col, start, end):
    
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
        ax.set_xlim(0, max(x_col))
    ax.xaxis.set_major_locator(plt.MaxNLocator(int(max_x_ticks)))
    ax.yaxis.set_major_locator(plt.MaxNLocator(int(max_y_ticks)))
    ax.margins(x=float(xmargin))
    ax.margins(y=float(ymargin))
    ax.set_title(title , fontsize=int(title_size), fontweight=title_bold)
    ax.set_xlabel(xlabel, fontsize=int(xylabelsize), fontweight =xybold)
    ax.set_ylabel(ylabel, fontsize=int(xylabelsize), fontweight=xybold)
    ax.tick_params(axis='x', labelsize=int(xticksize))
    ax.tick_params(axis='y', labelsize=int(yticksize))
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
    [sg.Text('Choose the theme of the plot', size=(70,1)), sg.Combo(values=plt.style.available, key='_THEME_', default_value='_classic_test_patch', readonly=True, size=(30,10))],
    [sg.Text('Enter the title of the plot', size=(70,1)), sg.Input(default_text='Response Curve', key='_TITLE_', enable_events=True)],
    [sg.Text('Font size of the title', size=(70,1)), sg.Input(key='_FS_', default_text='12', enable_events=True)], 
    [sg.Text('Fontweight of title: ', size=(70,1)), sg.Radio('Bold', "fw", default=True, key='_FW_'), sg.Radio('Regular', "fw", default=False)],
    [sg.Text('Enter the width of the plot (in inches)', size=(70,1)), sg.Input(default_text='10', key='_WIDTH_', enable_events=True)],
    [sg.Text('Enter the height of the plot (in inches)', size=(70,1)), sg.Input(default_text='6', key='_HEIGHT_', enable_events=True)],
    [sg.Text('Enter the line width for the plot', size=(70,1)), sg.Input(default_text='0.8', key='_LW_', enable_events=True)],
    [sg.Text('Enter the x-axis label of the plot', size=(70,1)), sg.Input(default_text='Scan', key='_XLABEL_', enable_events=True)],
    [sg.Text('Enter the y-axis label of the plot', size=(70,1)), sg.Input(default_text='Resistance',key='_YLABEL_', enable_events=True)],
    [sg.Text('Font size of the XY labels', size=(70,1)), sg.Input(key='_FSXY_', default_text='12', enable_events=True)], 
    [sg.Text('Fontweight of XY label: ', size=(70,1)), sg.Radio('Bold', "fwxy", default=True, key='_FWXY_'), sg.Radio('Regular', "fwxy", default=False)],
    [sg.Text('Enter the size of the x-tick labels: ', size=(70,1)), sg.Input(default_text='12', key='_XTICKSIZE_', enable_events=True)],
    [sg.Text('Enter the size of the y-ticks labels: ', size=(70,1)), sg.Input(default_text='12', key='_YTICKSIZE_', enable_events=True)],
    [sg.Text('Enter the desired number of ticks in the x-axis', size=(70,1)), sg.Input(default_text='3', key='_XTICKS_', enable_events=True)],
    [sg.Text('Enter the desired number of ticks in the y-axis', size=(70,1)), sg.Input(default_text='3', key='_YTICKS_', enable_events=True)],
    [sg.Text('Enter the % margin to be padded in the X-axis of the plot(float values from 0 to 1)', size=(70,1)), sg.Input(default_text='0', key='_XMARGIN_', enable_events=True)],
    [sg.Text('Enter the % margin to be padded in the Y-axis of the plot(float values from 0 to 1)', size=(70,1)), sg.Input(default_text='0.05', key='_YMARGIN_', enable_events=True)],
    [sg.Text('Do you require a legend in the plot?', size=(70,1)), sg.Radio('Yes', "legend", default=True, key='_LEGEND_'), sg.Radio('No', "legend", default=False)],
    [sg.Text('Enter the font size of the legend', size=(70,1)), sg.Input(key='_LZ_', enable_events=True, default_text='6')],
    [sg.Text('The pdf.fonttype used is type no 42 keeping in line with IEEE standards', size=(55,1))],
    [sg.Text('Even though the legend might not be visible on the canvas, it exists and can be viewed by saving the plot', size=(85,2))]]
    
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
    [sg.Listbox(values=y_cols, default_values=y_cols, select_mode='multiple', key='_DATA_', size=(30, 10))],
    [sg.Text('Black means selected and white means not selected')]]

    layout4=[
    [sg.Text('If you wish to plot a particular section of the graph, e.g, from the 700th data point to the 800th data point for the chosen Y-axis columns, then fill the following parameters. Otherwise please leave it blank to allow the program to plot all the data', size=(45,6))],
    [sg.Text('Enter the start index(eg. 800)', size=(45,1)), sg.Input(key='_SINDEX_', enable_events=True)],
    [sg.Text('Enter the end index(eg. 1000)', size=(45,1)), sg.Input(key='_EINDEX_', enable_events=True)],
    [sg.Button('Preview zoomed plot')]]
    

    layout_main=[
    [sg.Frame('Plot Parameters', layout=layout1)]]
    layout_data=[[sg.Frame('X-axis columns', layout=layout2), sg.Frame('Y-axis columns', layout=layout3)],
    [sg.Button('Preview plot')]]
    
    layout_zoom=[[sg.Frame('Optional row indexing to examine behaviour of a signal closely', layout=layout4)],
    [sg.Text('Press default to see the default plot again'), sg.Button('Default')]]

    layout_plot=[[sg.Canvas(size=(1100, 600), key='-CANVAS-', pad=(5,5))], 
    [sg.Button('Save Plot')]]

    layout=[[sg.TabGroup([[sg.Tab('Plot parameters', layout=layout_main, key='param')], [sg.Tab('Choose data', layout=layout_data, key='data')], [sg.Tab('Plot preview', layout=layout_plot, key='plot')], [sg.Tab('Zoomed plotting', layout=layout_zoom, key='zoom')]], key='tabgroup', enable_events=True)],
    [sg.Text('Press the button to leave the response curve dashboard and move to the feature extraction module'), sg.Button('Feature extraction dashboard')]]


    window = sg.Window('Plotting dashboard', layout=layout, grab_anywhere=False, finalize=True, size=(1200,800))

    figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, response(df, t_col_no, dat_col))
    window['tabgroup'].Widget.select(2)
    
    fl=0

    while True:
        event, v = window.Read()
        if event==sg.WIN_CLOSED or event=='Feature extraction dashboard':
            break

        if event=='Default':
            if figure_agg:
                delete_figure_agg(figure_agg)
            figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, response(df, t_col_no, dat_col))
            window['tabgroup'].Widget.select(2)
            fl=0


        if event=='Save Plot':
            if fl==1:
                save_plot_dashboard(preview_plot(df, v['_THEME_'], v['_WIDTH_'], v['_HEIGHT_'], v['_LW_'], v['_TITLE_'], v['_FW_'], v['_FS_'],  
                                                    v['_FSXY_'], v['_FWXY_'], v['_XLABEL_'], v['_YLABEL_'], v['_LEGEND_'], v['_LZ_'], v['_XTICKSIZE_'],  v['_YTICKSIZE_'], 
                                                    v['_XTICKS_'], v['_YTICKS_'], v['_XMARGIN_'], v['_YMARGIN_'], t_col, v['_DATA_'], False, False))
                
            elif fl==2:
                save_plot_dashboard(preview_plot(df, v['_THEME_'], v['_WIDTH_'], v['_HEIGHT_'], v['_LW_'], v['_TITLE_'], v['_FW_'], v['_FS_'],  
                                                    v['_FSXY_'], v['_FWXY_'], v['_XLABEL_'], v['_YLABEL_'], v['_LEGEND_'], v['_LZ_'], v['_XTICKSIZE_'],  v['_YTICKSIZE_'], 
                                                    v['_XTICKS_'], v['_YTICKS_'], v['_XMARGIN_'], v['_YMARGIN_'], t_col, v['_DATA_'], int(v['_SINDEX_']), int(v['_EINDEX_'])))
                
            elif fl==0:
                save_plot_dashboard(response(df, t_col_no, dat_col))
            continue

        if event=='Preview plot' or event=='Preview zoomed plot':
            if v['_DATA_'][0] is None:
                sg.popup_error('At least one y-axis column must be selected')
                continue
            elif v['_WIDTH_'] is '':
                sg.popup_error('Width field cannot be blank')
                continue
            elif v['_HEIGHT_'] is '':
                sg.popup_error('Height field cannot be blank')
                continue
            elif v['_TITLE_'] is '':
                sg.popup_error('Title field cannot be blank')
                continue
            elif v['_XLABEL_'] is '':
                sg.popup_error('X-axis label field cannot be blank')
                continue
            elif v['_YLABEL_'] is '':
                sg.popup_error('Y-axis label field cannot be blank')
                continue
            elif v['_XTICKS_'] is '':
                sg.popup_error('Max X ticks field cannot be blank')
                continue
            elif v['_YTICKS_'] is '':
                sg.popup_error('Max Y ticks field cannot be blank')
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
            else:
                pass
            
        if event=='Preview plot':
            if figure_agg:
                delete_figure_agg(figure_agg)
            if v['_XAXIS_'] is 'Index':
                t_col=df.index.values.tolist()
            else:
                t_col=df.iloc[:,(int(t_col_no)-1)]
            fig=preview_plot(df, v['_THEME_'], 10, 6, v['_LW_'], v['_TITLE_'], v['_FW_'], v['_FS_'],  
                            v['_FSXY_'], v['_FWXY_'], v['_XLABEL_'], v['_YLABEL_'], v['_LEGEND_'], v['_LZ_'], v['_XTICKSIZE_'],  v['_YTICKSIZE_'], 
                            v['_XTICKS_'], v['_YTICKS_'], v['_XMARGIN_'], v['_YMARGIN_'], t_col, v['_DATA_'], False, False)
            figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
            fl=1
            window['tabgroup'].Widget.select(2)

        if event=='Preview zoomed plot':
            if figure_agg:
                delete_figure_agg(figure_agg)
            if v['_XAXIS_'] is 'Index':
                t_col=df.index.values.tolist()
            else:
                t_col=df.iloc[:,(int(t_col_no)-1)]
            if v['_SINDEX_'] is '' or v['_EINDEX_'] is '':
                sg.popup_error('Either of the indexes are empty')
                continue
            fig=preview_plot(df, v['_THEME_'], 10, 6, v['_LW_'], v['_TITLE_'], v['_FW_'], v['_FS_'],  
                            v['_FSXY_'], v['_FWXY_'], v['_XLABEL_'], v['_YLABEL_'], v['_LEGEND_'], v['_LZ_'], v['_XTICKSIZE_'],  v['_YTICKSIZE_'], 
                            v['_XTICKS_'], v['_YTICKS_'], v['_XMARGIN_'], v['_YMARGIN_'], t_col, v['_DATA_'], int(v['_SINDEX_']), int(v['_EINDEX_']))
            figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
            fl=2
            window['tabgroup'].Widget.select(2)
            

    window.close()
    return

def conc_feature_plot_dash(dm, typemat):

    plot_basic_param_layout=[
    [sg.Text('Choose the theme of the plot', size=(70,1)), sg.Combo(values=plt.style.available, key='_THEME_', default_value='_classic_test_patch', readonly=True, size=(30,10))],
    [sg.Text('Enter the title of the plot', size=(70,1)), sg.Input(default_text='Concentration Feature Plot', key='_TITLE_', enable_events=True)],
    [sg.Text('Font size of the title', size=(70,1)), sg.Input(key='_FS_', default_text='12', enable_events=True)], 
    [sg.Text('Fontweight of title: ', size=(70,1)), sg.Radio('Bold', "fw", default=True, key='_FW_'), sg.Radio('Regular', "fw", default=False)],
    [sg.Text('Enter the width of the plot (in inches)', size=(70,1)), sg.Input(default_text='10', key='_WIDTH_', enable_events=True)],
    [sg.Text('Enter the height of the plot (in inches)', size=(70,1)), sg.Input(default_text='6', key='_HEIGHT_', enable_events=True)],
    [sg.Text('Enter the x-axis label of the plot', size=(70,1)), sg.Input(default_text='Concentration', key='_XLABEL_', enable_events=True)],
    [sg.Text('Enter the y-axis label of the plot', size=(70,1)), sg.Input(default_text='Feature',key='_YLABEL_', enable_events=True)],
    [sg.Text('Font size of the XY labels', size=(70,1)), sg.Input(key='_FSXY_', default_text='12', enable_events=True)],
    [sg.Text('Enter the size of the x-tick labels: ', size=(70,1)), sg.Input(default_text='12', key='_XTICKSIZE_', enable_events=True)],
    [sg.Text('Enter the size of the y-ticks labels: ', size=(70,1)), sg.Input(default_text='12', key='_YTICKSIZE_', enable_events=True)], 
    [sg.Text('Enter the size of the marker in the scatter plot', size=(70,1)), sg.Input(default_text='25', key='_MSIZE_', enable_events=True)],
    [sg.Text('Fontweight of XY label: ', size=(70,1)), sg.Radio('Bold', "fwxy", default=True, key='_FWXY_'), sg.Radio('Regular', "fwxy", default=False)],
    [sg.Text('Enter the font size of the legend', size=(70,1)), sg.Input(key='_LZ_', enable_events=True, default_text='6')]]
    
    
    note_layout=[[sg.Text('The pdf.fonttype used is type no 42 keeping in line with IEEE standards', size=(55,1))],
    [sg.Text("For subscript in x-label, y-label or title enter data in the following format 'Concentration of $H_{2}$' to print the same text with H2 having 2 as subscript['Concentration of' is just for demonstration purposes](dollar signs and curly braces must be included. Quote signs not to be included)", size=(85, 5))],
    [sg.Text("For superscript, enter data in the following format $2^{x}$ for 2 exponent x")],
    [sg.Text('Even though the legend might not be visible on the canvas, it exists and can be viewed by saving the plot', size=(85,2))]]

    plot_basic_param_layout.append([sg.Frame('Note', layout=note_layout)])

    layout_plot=[[sg.Canvas(size=(1100, 600), key='-CANVAS-', pad=(5,5))], 
    [sg.Button('Save Plot')]]

    dm=dm.reset_index()
    header_list = list(dm.columns)
    data = dm[0:].values.tolist()
    dm=dm.set_index(dm.columns[0])

    table_layout=[
    [sg.Table(values=data, headings=header_list,
        enable_events=False, key='_TABLE_', 
        auto_size_columns=False,  justification='left',    
        hide_vertical_scroll=False, vertical_scroll_only=False, display_row_numbers=False
    )]]

    if typemat==1:
        x_cols=[]
        x_cols=dm.columns.tolist()
    
        y_cols=[]
        y_cols=dm.columns.tolist()
        layout2_type1=[
        [sg.Text('Choose the X-axis column', size=(45,1)), sg.Listbox(values=x_cols, default_values=[x_cols[0],], key='_XAXIS_', size=(30, 6), select_mode='multiple')],
        [sg.Text('Choose the Y-axis feature column', size=(45,1)), sg.Combo(values=y_cols, default_value=y_cols[1], key='_FEATURE_', size=(30, 6), readonly=True)],
        [sg.Text('Black means selected and white means not selected in the listbox')],
        [sg.Button('Plot')]]
        
        #label_layout=[[sg.Text('Please enter customized labels if default labels are unsatisfcatory. Number of expected arguments are {}'.format())],
        #[sg.Input(key='_LBL_', default_text='')]]

        type1_data_layout=[
        [sg.Text('Please use the basic plot parameters tab to enter title, xlabels, ylabels, etc. before using the current tab for plotting type I feature-conc plot')],
        [sg.Frame('Data selection', layout=layout2_type1)],
        [sg.Text('', size=(85,3))],
        [sg.Text('Multiple X axis columns can be chosen in case of same unit concentration columns. If plotting feature vs feature, please choose one X axis feature column for accurate results', size=(85, 3))],
        [sg.Text('Labels will be created as "index_column name_concentration value"')]]

        layout=[[sg.TabGroup([[sg.Tab('Current Data matrix', layout=table_layout, key='table')], [sg.Tab('Basic Plot Parameters', layout=plot_basic_param_layout, key='plotparam')], [sg.Tab('Type I plot parameters', layout=type1_data_layout, key='type1')], [sg.Tab('Plot preview', layout=layout_plot, key='plot')] ], key='tabgroup', enable_events=True)],
        [sg.Text('Choose this option to leave the plotting dashboard and go back to the data matrix dashboard'), sg.Button('Data Matrix Dashboard')]]
        
        window = sg.Window('Type I Plotting dashboard', layout=layout, grab_anywhere=False, finalize=True, size=(1200,800))
    if typemat==2:
        x_cols=[]
        x_cols=dm.columns.tolist()
    
        y_cols=[]
        y_cols=dm.columns.tolist()

        layout1_type2=[[sg.Text('Choose the X-axis concentration column', size=(45,1)), sg.Combo(values=x_cols, default_value=x_cols[0], key='_XAXISTYPE2_', size=(30, 1), readonly=True)],
        [sg.Text('Choose the sensors for which you want to plot the feature against the concentration Y-axis', size=(45,2)), sg.Listbox(values=y_cols, default_values=[y_cols[0],], select_mode='multiple', key='_FEATURETYPE2_', size=(30, 6))],
        [sg.Text('Black means selected and white means not selected')]]
    
        type2_data_layout=[
        [sg.Text('Please use the basic plot parameters tab to enter title, xlabels, ylabels, etc. before using the current tab for plotting type II feature-conc plot')],
        [sg.Frame('X-axis: Concentration and Y-axis: Sensor feature', layout=layout1_type2)],
        [sg.Text('Labels will be created by sensor names')],
        [sg.Button('Plot Sensor Feature(Y) vs Concentration(X)')]]

        layout=[[sg.TabGroup([[sg.Tab('Current Data matrix', layout=table_layout, key='table')], [sg.Tab('Basic Plot Parameters', layout=plot_basic_param_layout, key='plotparam')], [sg.Tab('Type II plot parameters', layout=type2_data_layout, key='type2')], [sg.Tab('Plot preview', layout=layout_plot, key='plot')] ], key='tabgroup', enable_events=True)],
        [sg.Text('Choose this option to leave the plotting dashboard and go back to the data matrix dashboard'), sg.Button('Data Matrix Dashboard')]]
        
        window = sg.Window('Type II Plotting dashboard', layout=layout, grab_anywhere=False, finalize=True, size=(1200,800))
    

    
    window['tabgroup'].Widget.select(0)
    figure_agg = None

    while True:
        event, v = window.Read()
        if event==sg.WIN_CLOSED:
            break
        if event=='Save Plot':
            if typemat==1:
                save_plot_dashboard(conc_feature_preview_type1(dm, v['_THEME_'], v['_WIDTH_'], v['_HEIGHT_'], v['_TITLE_'], v['_FW_'], v['_FS_'],  
                                          v['_FSXY_'], v['_FWXY_'], v['_XLABEL_'], v['_YLABEL_'], v['_LZ_'], v['_XTICKSIZE_'], v['_YTICKSIZE_'], v['_MSIZE_'], v['_XAXIS_'], v['_FEATURE_']))
            elif typemat==2:
                save_plot_dashboard(conc_feature_preview_type2(dm, v['_THEME_'], v['_WIDTH_'], v['_HEIGHT_'], v['_TITLE_'], v['_FW_'], v['_FS_'],  
                                          v['_FSXY_'], v['_FWXY_'], v['_XLABEL_'], v['_YLABEL_'], v['_LZ_'], v['_XTICKSIZE_'], v['_YTICKSIZE_'], v['_MSIZE_'], v['_XAXISTYPE2_'], v['_FEATURETYPE2_']))




        if event=='Plot' or event=='Plot Sensor Feature(Y) vs Concentration(X)':
            if v['_TITLE_'] is '':
                sg.popup_error('Title field cannot be blank')
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
            elif v['_FSXY_'] is '':
                sg.popup_error('XY label font size field cannot be blank')
                continue
            elif v['_LZ_'] is '':
                sg.popup_error('Legend font size field cannot be blank')
                continue
            elif v['_XTICKSIZE_'] is '':
                sg.popup_error('X-tick font size field cannot be blank')
                continue
            elif v['_YTICKSIZE_'] is '':
                sg.popup_error('Y-tick font size field cannot be blank')
                continue
            elif v['_MSIZE_'] is '':
                sg.popup_error('Marker size field cannot be blank')
                continue
            
        if event=='Plot':
            if figure_agg:
                delete_figure_agg(figure_agg)
            fig=conc_feature_preview_type1(dm, v['_THEME_'], 10, 6, v['_TITLE_'], v['_FW_'], v['_FS_'],  
                                          v['_FSXY_'], v['_FWXY_'], v['_XLABEL_'], v['_YLABEL_'], v['_LZ_'], v['_XTICKSIZE_'], v['_YTICKSIZE_'], v['_MSIZE_'], v['_XAXIS_'], v['_FEATURE_'])
            figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
            window['tabgroup'].Widget.select(3)
            

        if event=='Plot Sensor Feature(Y) vs Concentration(X)':
            if figure_agg:
                delete_figure_agg(figure_agg)
            fig=conc_feature_preview_type2(dm, v['_THEME_'], 10, 6, v['_TITLE_'], v['_FW_'], v['_FS_'],  
                                          v['_FSXY_'], v['_FWXY_'], v['_XLABEL_'], v['_YLABEL_'], v['_LZ_'], v['_XTICKSIZE_'], v['_YTICKSIZE_'], v['_MSIZE_'], v['_XAXISTYPE2_'], v['_FEATURETYPE2_'])
            figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
            window['tabgroup'].Widget.select(3)
        if event=='Data Matrix Dashboard':
            break

    window.close()
    return


  
"""    

def conc_feature_plot_dash_type2(dm, sens_start):
    layout1=[
    [sg.Text('Enter the title of the plot', size=(45,1)), sg.Input(default_text='Concentration vs Sensor Feature Plot', key='_TITLE_', enable_events=True)],
    [sg.Text('Enter the width of the plot (in inches)', size=(45,1)), sg.Input(default_text='8', key='_WIDTH_', enable_events=True)],
    [sg.Text('Enter the height of the plot (in inches)', size=(45,1)), sg.Input(default_text='5', key='_HEIGHT_', enable_events=True)],
    [sg.Text('Enter the x-axis label of the plot', size=(45,1)), sg.Input(default_text='Concentration', key='_XLABEL_', enable_events=True)],
    [sg.Text('Enter the y-axis label of the plot', size=(45,1)), sg.Input(default_text='Sensor Feature',key='_YLABEL_', enable_events=True)],
    [sg.Text('The pdf.fonttype used is type no 42 keeping in line with IEEE standards', size=(55,1))]]

    
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

"""

def conc_feature_preview_type1(dm, theme, width, height, title, title_bold, title_size, xylabelsize, xybold, xlabel, ylabel, legend_size, xticksize, yticksize, msize, concX, featureY):
    fig_size=(float(width), float(height))


    """Figure creation using matplotlib"""
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['ps.fonttype'] = 42
    mpl.rcParams['font.family'] = 'Arial'

    fig = plt.figure(figsize=fig_size)
    plt.style.use(theme)
    ax = fig.add_subplot(111)

    
    if title_bold is True:
        title_bold='bold'
    else:
        title_bold='regular'

    if xybold is True:
        xybold='bold'
    else:
        xybold='regular'

    labels=[]
    y_col_no=dm.columns.get_loc(featureY)
    for val in concX:
        x_col_no= dm.columns.get_loc(val)
        index_val=dm.index.values.tolist()
        colname=dm.columns[x_col_no]
        for i in range(0, dm.shape[0]):
            ax.scatter(dm.iloc[i, x_col_no], dm.iloc[i, y_col_no], alpha=0.6, s=float(msize))
            label=index_val[i]+"_"+colname+"_"+(val[i])
            labels.append(label)       
    ax.legend(labels=labels, loc='upper left', bbox_to_anchor=(1,1))


    

    
    ax.set_title(title , fontsize=int(title_size), fontweight=title_bold)
    ax.set_xlabel(xlabel, fontsize=int(xylabelsize), fontweight =xybold)
    ax.set_ylabel(ylabel, fontsize=int(xylabelsize), fontweight=xybold)
    ax.tick_params(axis='x', labelsize=int(xticksize))
    ax.tick_params(axis='y', labelsize=int(yticksize))

    return fig



def conc_feature_preview_type2(dm, theme, width, height, title, title_bold, title_size, xylabelsize, xybold, xlabel, ylabel, legend_size, xticksize, yticksize, msize, concX, sensorsY):
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

    
    for val in sensorsY:
        ax.scatter(dm.loc[:, concX], dm.loc[:,val], label=val, alpha=0.6, s=float(msize))
        ax.legend(loc='upper left', bbox_to_anchor=(1,1), prop={'size': int(legend_size)})
        

    


    ax.set_title(title , fontsize=int(title_size), fontweight=title_bold)
    ax.set_xlabel(xlabel, fontsize=int(xylabelsize), fontweight =xybold)
    ax.set_ylabel(ylabel, fontsize=int(xylabelsize), fontweight=xybold)
    ax.tick_params(axis='x', labelsize=int(xticksize))
    ax.tick_params(axis='y', labelsize=int(yticksize))



    return fig
    









if __name__ == '__main__':
  response()
    