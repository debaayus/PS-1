import pandas as pd
import sys 
import numpy as np

def find_sensitivity(sensor,poi, df):

    ser1=df.loc[:,sensor]
    sensitivity=0
    baseline=0
    print(ser1.head(30))
    for i in range(poi-30,poi):
        baseline+=ser1[i]
    baseline/=30
    sens=[]
    
    for i in range(poi-90, poi+210):
        sens.append(abs((ser1[i]-baseline)/baseline))
    sensitivity = max(sens)
    return sensitivity

    

def grad(x):
    for i in range(x.size-1):
        x[i]=x[i+1]-x[i]
    return x

def recovery_slope(sensor,poi,df):
    ser1=df.ix[poi-90:poi+210,sensor]
    gradient = grad(ser1)
    recslope = gradient.max()
    return recslope

def response_slope(sensor,poi,df):
    ser1=df.ix[poi-90:poi+210,sensor]
    gradient = grad(ser1)
    resslope = gradient.min()
    return resslope

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
    print(df.columns)
    print(find_sensitivity(df.columns[2],900, df))


    


if __name__ == '__main__':
    main()