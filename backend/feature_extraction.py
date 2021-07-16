import pandas as pd
import sys 
import numpy as np
from scipy.integrate import simps

def base_line(poi,ser1):
    baseline=0
    for i in range(poi-30,poi):
        baseline+=ser1[i]
    baseline/=30
    return baseline

def find_sensitivity(sensor,poi, df,next):

    ser1=df.iloc[:,sensor]
    sensitivity=0
    baseline=base_line(poi,ser1)
    sens=[]
    
    for i in range(poi,poi+next):
        sens.append(abs((ser1[i]-baseline)/baseline))
    sensitivity = max(sens)
    return sensitivity

    

def grad(x,poi,next,gap):
    gradient=[]
    for i in range(poi+1,poi+next):
        gradient.append((x[i]-x[i-1])/gap)
    return gradient

def recovery_slope(sensor,poi,df,next,gap):
    ser1=df.iloc[poi-1:poi+next-1,sensor]
    gradient = grad(ser1,poi,next,gap)
    recslope = max(gradient)
    return recslope

def response_slope(sensor,poi,df,next,gap):
    ser1=df.iloc[poi-1:poi+next-1,sensor]
    gradient = grad(ser1,poi,next,gap)
    resslope = min(gradient)
    return resslope

def tip(ser,poi,next):
    tipp=ser[poi]
    index=poi
    for i in range(poi,poi+next):
        tipp=min(ser[i],tipp)
        if tipp == ser[i]:
            index = i            
    return index

def response_time(sensor,poi,df,next,gap):
    ser1=df.iloc[:,sensor]
    baseline =base_line(poi,ser1)
    ser2=df.iloc[poi-1:poi+next-1,sensor]
    index_tip = tip(ser2,poi,next)
    delR = (baseline-ser2[index_tip])*0.90
    R90 = ser2[poi] -delR
    index1=poi
    index1min = abs(ser2[poi]-R90)
    for i in range(poi,index_tip+1):
        index1min = min(index1min,abs(ser2[i]-R90))
        if index1min == abs(ser2[i]-R90):
            index1 = i
    index2 = index1-1
    time1 = index1 * gap
    time2 = index2 * gap
    time = ((((R90-ser2[index2])/(ser2[index1]-ser2[index2]))*(time1-time2))+time2)-(poi*gap)
    return time

def recovery_time(sensor,poi,df,next,gap):
    ser1=df.iloc[:,sensor]
    baseline =base_line(poi+next,ser1)
    ser2=df.iloc[poi-1:poi+next-1,sensor]
    index_tip = tip(ser2,poi,next)
    delR = (baseline-ser2[index_tip])*0.90
    R90 = ser2[index_tip]+delR
    index1 = index_tip
    index1min = abs(ser2[index_tip]-R90)
    for i in range(index_tip,poi+next):
        index1min = min(index1min,abs(ser2[i]-R90))
        if index1min == abs(ser2[i]-R90):
            index1 = i
    index2 = index1-1
    time1 = index1 * gap
    time2 = index2 * gap
    time = ((((R90-ser2[index2])/(ser2[index1]-ser2[index2]))*(time1-time2))+time2)-(index_tip*gap)
    return time

def integral_area(sensor,poi,df,points,gap):
    ser1 = df.iloc[poi:poi+points+1,sensor]
    area = simps(ser1,dx=gap)
    return area

def matrix_type1(df,list_poi,gap,points,sensor_name):
    sensor_list=df.columns.tolist()
    sensor=sensor_list.index(sensor_name)
    num_poi=len(list_poi)
    list_poi.sort(reverse=False)
    num_rows = df.shape[0]
    """sensor = int(input('Enter the sensor column number: '))
    points = int(input('Enter the time in sec for which you have to calculate integral area: '))"""
    points = points // gap
    poi = list_poi[0]//gap
    if num_poi==1:
        next = num_rows-((list_poi[0])//gap)
    else:
        next = (list_poi[1]-list_poi[0])//gap
    sens = find_sensitivity(sensor,poi,df,next)
    recslope = recovery_slope(sensor,poi,df,next,gap)
    resslope = response_slope(sensor,poi,df,next,gap)
    restime = response_time(sensor,poi,df,next,gap)
    rectime = recovery_time(sensor,poi,df,next,gap)
    area = integral_area(sensor,poi,df,points,gap)
    Ratio = 1-sens
    sens *=100
    features = [[sens,recslope,resslope,rectime,restime,area,Ratio]]
    df1 = pd.DataFrame(features,columns=['Response(in %)','Recovery Slope', 'Response Slope', 'Recovery Time', 'Response Time', 'Integral Area','Ratio'])
    for i in range(1,num_poi):
        poi = list_poi[i]//gap
        if i+1==num_poi:
            next = num_rows-((list_poi[i])//gap)
        else:
            next = (list_poi[i+1]-list_poi[i])//gap
        sens = find_sensitivity(sensor,poi,df,next)
        recslope = recovery_slope(sensor,poi,df,next,gap)
        resslope = response_slope(sensor,poi,df,next,gap)
        restime = response_time(sensor,poi,df,next,gap)
        rectime = recovery_time(sensor,poi,df,next,gap)
        area = integral_area(sensor,poi,df,points,gap)
        Ratio = 1-sens
        sens *= 100
        features = [[sens,recslope,resslope,restime,rectime,area,Ratio]]
        df1 = df1.append(pd.DataFrame(features,columns=['Response(in %)','Recovery Slope', 'Response Slope', 'Recovery Time', 'Response Time', 'Integral Area','Ratio']),ignore_index=True)
    index_col = []
    for i in range (1,num_poi+1):
        index_col.append('Signal '+str(i))
    df1.insert(loc=0,column='Signal',value=index_col)
    df1.set_index("Signal",inplace=True)
    return df1

def matrix_type2(feature,df,list_poi,gap,total_sensor, dat_col, points):
    num_rows=df.shape[0]
    num_poi=len(list_poi)
    """total_sensor = int(input('Enter the total number of sensors:'))
    start = int(input('Enter the starting column number: '))"""
    start=int(dat_col)-1
    column_name = df.columns[start: start+total_sensor].tolist()
    df1 = pd.DataFrame(columns=column_name)
    if feature=='Response(in %)':
        for i in range(num_poi):
            poi = list_poi[i]//gap
            if i+1==num_poi:
                next = num_rows-((list_poi[i])//gap)
            else:
                next = (list_poi[i+1]-list_poi[i])//gap
            sens=[]
            for i in range (start,start+total_sensor):
                sens.append(find_sensitivity(i,poi,df,next)*100)
            df1=df1.append(pd.DataFrame([sens],columns=column_name),ignore_index=True)
    elif feature=='Recovery Slope':
        for i in range(num_poi):
            poi = list_poi[i]//gap
            if i+1==num_poi:
                next = num_rows-((list_poi[i])//gap)
            else:
                next = (list_poi[i+1]-list_poi[i])//gap
            sens=[]
            for i in range (start,start+total_sensor):
                sens.append(response_slope(i,poi,df,next,gap))
            df1=df1.append(pd.DataFrame([sens],columns=column_name),ignore_index=True)
    elif feature=='Response Slope':
        for i in range(num_poi):
            poi = list_poi[i]//gap
            if i+1==num_poi:
                next = num_rows-((list_poi[i])//gap)
            else:
                next = (list_poi[i+1]-list_poi[i])//gap
            sens=[]
            for i in range (start,start+total_sensor):
                sens.append(recovery_slope(i,poi,df,next,gap))
            df1=df1.append(pd.DataFrame([sens],columns=column_name),ignore_index=True)
    elif feature=='Recovery Time':
        for i in range(num_poi):
            poi = list_poi[i]//gap
            if i+1==num_poi:
                next = num_rows-((list_poi[i])//gap)
            else:
                next = (list_poi[i+1]-list_poi[i])//gap
            sens=[]
            for i in range (start,start+total_sensor):
                sens.append(response_time(i,poi,df,next,gap))
            df1=df1.append(pd.DataFrame([sens],columns=column_name),ignore_index=True)
    elif feature=='Response Time':
        for i in range(num_poi):
            poi = list_poi[i]//gap
            if i+1==num_poi:
                next = num_rows-((list_poi[i])//gap)
            else:
                next = (list_poi[i+1]-list_poi[i])//gap
            sens=[]
            for i in range (start,start+total_sensor):
                sens.append(recovery_time(i,poi,df,next,gap))
            df1=df1.append(pd.DataFrame([sens],columns=column_name),ignore_index=True)
    elif feature=='Integral Area':
        points = points // gap
        for i in range(num_poi):
            poi = list_poi[i]//gap
            if i+1==num_poi:
                next = num_rows-((list_poi[i])//gap)
            else:
                next = (list_poi[i+1]-list_poi[i])//gap
            sens=[]
            for i in range (start,start+total_sensor):
                sens.append(integral_area(i,poi,df,points,gap))
            df1=df1.append(pd.DataFrame([sens],columns=column_name),ignore_index=True)
    elif feature=='Ratio':
        for i in range(num_poi):
            poi = list_poi[i]//gap
            if i+1==num_poi:
                next = num_rows-((list_poi[i])//gap)
            else:
                next = (list_poi[i+1]-list_poi[i])//gap
            sens=[]
            for i in range (start,start+total_sensor):
                sens.append(1-find_sensitivity(i,poi,df,next))
            df1=df1.append(pd.DataFrame([sens],columns=column_name),ignore_index=True)
    index_col = []
    for i in range (1,num_poi+1):
        index_col.append('Signal '+str(i))
    df1.insert(loc=0,column='Signal',value=index_col)
    df1.set_index("Signal",inplace=True)
    return df1
        
def df_creation():
    filename = sys.argv[1]

    try:

        df = pd.read_csv(filename, encoding = 'utf-16', skiprows=16, delimiter='\t', index_col='Scan') 
    except:
        df = pd.read_csv(filename, encoding = 'utf-8', skiprows=0, delimiter='|', index_col=0) ## for
    return df 


"""
Removed the pre-processing module. Can directly run from this script. Use the command below to test:

python feature_extraction.py ../test_data/170619a2-delim-whitespace.csv
python feature_extraction.py ../test_data/test1-delim-line.csv

"""
def main():


    df=df_creation()
    gap = int(input('Enter the difference of time between two consecutive readings (in sec): '))
    num_poi = int(input('Enter the number of poi:'))
    poi = []
    for i in range(num_poi):
        poi.append(int(input()))
    """print(find_sensitivity(sensor+1,poi,df,next))
    print(response_slope(sensor+1,poi, df,next,gap))
    print(recovery_slope(sensor+1,poi, df,next,gap))
    print(response_time(sensor+1,poi, df,next,gap))
    print(recovery_time(sensor+1,poi, df,next,gap))
    print(integral_area(sensor+1,poi, df,next,gap))"""
    mtype = int(input('enter the type of matrix you want(1/2): '))
    if mtype == 1:
        df1 = matrix_type1(df,poi,gap,60,1)
    elif mtype==2:
        feature = int(input("Enter the feature number(1-Response(in %)  2-response slope  3-recovery slope  4-response time  5-recovery time  6-integral area 7-Ratio): "))
        df1 = matrix_type2(feature,df,poi,gap,8,1)
    print(df1)
    


if __name__ == '__main__':
    main()