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

def matrix_type1(df,num_poi,list_poi,gap,points,sensor):
    num_rows = df.shape[0]
    """sensor = int(input('Enter the sensor column number: '))
    points = int(input('Enter the time in sec for which you have to calculate integral area: '))"""
    points = points // gap
    poi = list_poi[0]//gap
    next = (list_poi[1]-list_poi[0])//gap
    sens = find_sensitivity(sensor,poi,df,next)
    recslope = recovery_slope(sensor,poi,df,next,gap)
    resslope = response_slope(sensor,poi,df,next,gap)
    restime = response_time(sensor,poi,df,next,gap)
    rectime = recovery_time(sensor,poi,df,next,gap)
    area = integral_area(sensor,poi,df,points,gap)
    Ratio = 1-sens
    sens *=100
    features = [[sens,recslope,resslope,restime,rectime,area,Ratio]]
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
    return df1

def matrix_type2(feature,df,poi,next,gap):
    num_rows=df.shape[0]
    total_sensor = int(input('Enter the total number of sensors:'))
    start = int(input('Enter the starting column number: '))
    column_name = []
    for i in range (1,1+total_sensor):
        column_name.append(i)
    df1 = pd.DataFrame(columns=column_name)
    if feature==1:
        while poi+next<=num_rows:
            sens=[]
            for i in range (start,start+total_sensor):
                sens.append(find_sensitivity(i,poi,df,next))
            df1=df1.append(pd.DataFrame([sens],columns=column_name),ignore_index=True)
            poi=poi+next
    elif feature==2:
        while poi+next<=num_rows:
            sens=[]
            for i in range (start,start+total_sensor):
                sens.append(response_slope(i,poi,df,next,gap))
            df1=df1.append(pd.DataFrame([sens],columns=column_name),ignore_index=True)
            poi=poi+next
    elif feature==3:
        while poi+next<=num_rows:
            sens=[]
            for i in range (start,start+total_sensor):
                sens.append(recovery_slope(i,poi,df,next,gap))
            df1=df1.append(pd.DataFrame([sens],columns=column_name),ignore_index=True)
            poi=poi+next
    elif feature==4:
        while poi+next<=num_rows:
            sens=[]
            for i in range (start,start+total_sensor):
                sens.append(response_time(i,poi,df,next,gap))
            df1=df1.append(pd.DataFrame([sens],columns=column_name),ignore_index=True)
            poi=poi+next
    elif feature==5:
        while poi+next<=num_rows:
            sens=[]
            for i in range (start,start+total_sensor):
                sens.append(recovery_time(i,poi,df,next,gap))
            df1=df1.append(pd.DataFrame([sens],columns=column_name),ignore_index=True)
            poi=poi+next
    elif feature==6:
        points = int(input('Enter the time in sec for which you have to calculate integral area: '))
        points = points // gap
        while poi+next<=num_rows:
            sens=[]
            for i in range (start,start+total_sensor):
                sens.append(integral_area(i,poi,df,points,gap))
            df1=df1.append(pd.DataFrame([sens],columns=column_name),ignore_index=True)
            poi=poi+next
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
    type = int(input('enter the type of matrix you want(1/2): '))
    if type == 1:
        df1 = matrix_type1(df,num_poi,poi,gap,60,1)
    elif type==2:
        feature = int(input("Enter the feature number(1-sensitivity  2-response slope  3-recovery slope  4-response time  5-recovery time  6-integral area): "))
        df1 = matrix_type2(feature,df,poi,next,gap)
    print(df1)
    


if __name__ == '__main__':
    main()