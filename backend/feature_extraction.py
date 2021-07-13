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

def matrix_type1(df,poi,next,gap):
    num_rows = df.shape[0]
    sensor = int(input('Enter the sensor number: '))
    points = int(input('Enter the time in sec for which you have to calculate integral area: '))
    points = points // gap
    sens = find_sensitivity(sensor,poi,df,next)
    recslope = recovery_slope(sensor,poi,df,next,gap)
    resslope = response_slope(sensor,poi,df,next,gap)
    restime = response_time(sensor,poi,df,next,gap)
    rectime = recovery_time(sensor,poi,df,next,gap)
    area = integral_area(sensor,poi,df,points,gap)
    features = [[sens,recslope,resslope,restime,rectime,area]]
    df1 = pd.DataFrame(features,columns=['Sensitivity','Recovery Slope' 'Response Slope', 'Recovery Time', 'Response Time', 'Integral Area'])
    poi = poi+next
    while poi+next <= num_rows:
        sens = find_sensitivity(sensor,poi,df,next)
        recslope = recovery_slope(sensor,poi,df,next,gap)
        resslope = response_slope(sensor,poi,df,next,gap)
        restime = response_time(sensor,poi,df,next,gap)
        rectime = recovery_time(sensor,poi,df,next,gap)
        area = integral_area(sensor,poi,df,points,gap)
        features = [[sens,recslope,resslope,restime,rectime,area]]
        df1 = df1.append(pd.DataFrame(features,columns=['Sensitivity','Recovery Slope' 'Response Slope', 'Recovery Time', 'Response Time', 'Integral Area']),ignore_index=True)
        poi =poi+next
    return dm1
        



def df_creation():
    filename = sys.argv[1]

    try:

        df = pd.read_csv(filename, encoding = 'utf-16', skiprows=16, delimiter='\t', index_col='Scan') 
        print(df.head())
    except:
        df = pd.read_csv(filename, encoding = 'utf-8', skiprows=0, delimiter='|', index_col=0) ## for
        print(df.head())
    return df 


"""
Removed the pre-processing module. Can directly run from this script. Use the command below to test:

python feature_extraction.py ../test_data/170619a2-delim-whitespace.csv
python feature_extraction.py ../test_data/test1-delim-line.csv

"""
def main():


    df=df_creation()
    gap = int(input('Enter the difference of time between two consecutive readings (in sec): '))
    poi = int(input('Enter the poi (in sec): '))
    poi=poi//gap
    next = int(input('Enter the gap between two consecutive poi (in sec): '))
    next=next//gap
    """print(find_sensitivity(sensor+1,poi,df,next))
    print(response_slope(sensor+1,poi, df,next,gap))
    print(recovery_slope(sensor+1,poi, df,next,gap))
    print(response_time(sensor+1,poi, df,next,gap))
    print(recovery_time(sensor+1,poi, df,next,gap))
    print(integral_area(sensor+1,poi, df,next,gap))"""
    df1 = matrix_type1(df,poi,next,gap)
    print(df1)

    


if __name__ == '__main__':
    main()