import pandas as pd
import sys 
import numpy as np

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

def tip(ser):
    tipp=ser[0]
    for i in ser:
        tipp=min(i,tipp)
    return tipp

def response_time(sensor,poi,df,next,gap):
    ser1=df.iloc[:,sensor]
    baseline =base_line(poi,ser1)
    ser2=df.iloc[poi-1:poi+next-1,sensor]
    tipp = tip(ser2)
    delR = (baseline-tipp)*0.90
    R90 = ser2[poi]-delR

"""def response_time(sensor,poi,df):
    ser1=df.iloc[:,sensor]
    baseline=base_line(poi,ser1)
    ser2=df.iloc[poi-1:poi+299,sensor]
    tipp = tip(poi,ser2)
    delR=(baseline-tipp)*0.90
    R90 = ser2[poi]-delR
    index1 = min(abs(ser1[poi:tipp]-R90)) +  poi-1
    index2 = index1 -1
    time = ((((R90-ser1[index2])/(ser1[index1]-ser1[index2]))*(ser1[index1]-ser1[index2]))+ser1[index2])-ser1[poi]
    return time
"""
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
    poi=poi/gap
    next = int(input('Enter the gap between two consecutive poi (in sec): '))
    next=next/gap
    sensor = int(input('Enter the sensor number: '))
    print(find_sensitivity(sensor+1,poi,df,next))
    print(response_slope(sensor+1,poi, df,next,gap))
    print(recovery_slope(sensor+1,poi, df,next,gap))
"""    print(response_time(2,300, df))"""



    


if __name__ == '__main__':
    main()