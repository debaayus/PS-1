from preprocessing import *

def find_sensitivity(sensor,poi,df):

    ser1=df.ix[:,sensor]
    sensitivity=0
    baseline=0
    for i in range(poi-30,poi):
        baseline+=ser1[i]
    baseline/=30
    for i in range(poi-90,poi+210):
        sens = (abs(ser1[i]-baseline))/baseline
        sensitivity=max(sensitivity,sens)
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

def main():
    print(find_sensitivity(1,90,df))
    


if __name__ == '__main__':
    main()