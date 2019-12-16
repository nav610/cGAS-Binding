import argparse
import numpy as np
#import matplotlib.plt as plt

parser=argparse.ArgumentParser()
parser.add_argument("-grid","--grid",help="grid file to graph")
parser.add_argument("-title","--title",help="title of plot")
args=parser.parse_args()

arr=(551,62)
arr = np.zeros(arr)

def convert_CV2(value):
    return(int(value*100))

def convert_CV1(value):
    return(int(10*value+31.4))

data=[]
f = open(args.grid)
for i in f.readlines()[9:]:
    if len(i.strip()) ==0:
        pass
    else:data.append(i)

for row in data:
    #print(row.split()[0],row.split()[1])
    CV2_index=convert_CV2(np.round(float(row.split()[0]),2))
    CV1_index=convert_CV1(np.round(float(row.split()[1]),2))
    bias=float(row.split()[2])
    print(int(CV2_index),int(CV1_index))
    arr[CV2_index,CV1_index]=bias
