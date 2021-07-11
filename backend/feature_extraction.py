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
    """R90 = ser2[poi]-delR
    index1= abs(ser2[poi]-R90)
    for i in range(poi,index_tip+1):
        index1 = min(index1,abs(ser2[i]-R90))
    index1 = index1 + poi -1
    index2 = index1 -1
    time = ((((R90-ser1[int(index2)])/(ser1[int(index1)]-ser1[int(index2)]))*(int(index1)*gap-int(index2)*gap))+int(index2)*gap)+poi*gap"""        
    time = (delR/(ser1[poi]-ser1[index_tip])*(abs(index_tip-poi))*gap)
    return time

def recovery_time(sensor,poi,df,next,gap):
    ser1=df.iloc[:,sensor]
    baseline =base_line(poi+next,ser1)
    ser2=df.iloc[poi-1:poi+next-1,sensor]
    index_tip = tip(ser2,poi,next)
    delR = (baseline-ser2[index_tip])*0.90
    time = (delR/(ser1[poi+next]-ser1[index_tip])*(abs(index_tip-poi+next))*gap)
    return time

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
    sensor = int(input('Enter the sensor number: '))
    print(find_sensitivity(sensor+1,poi,df,next))
    print(response_slope(sensor+1,poi, df,next,gap))
    print(recovery_slope(sensor+1,poi, df,next,gap))
    print(response_time(sensor+1,poi, df,next,gap))
    print(recovery_time(sensor+1,poi, df,next,gap))



    


if __name__ == '__main__':
    main()