import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import matplotlib.ticker as ticker
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import FormatStrFormatter
parser=argparse.ArgumentParser()
parser.add_argument("-grid","--grid",help="grid file to graph")
parser.add_argument("-name","--name",help="title of plot")
parser.add_argument("-frames","--frames",help="frame list")

args=parser.parse_args()

def convert_CV2(value):
    return(int(value*100))

def convert_CV1(value):
    return(int(10*value+31.4))

def find_nearest(array,value):
    array = np.asarray(array)
    idx = (np.abs(array-value)).argmin()
    return array[idx]

def make_line(point1,point2):
	m = (point2[1]-point1[1])/(point2[0]-point1[0])
	b = point2[1]-m*point2[0]
	x = np.arange(point1[0],point2[0],1)
	y = x*m + b 
	values = []
	values.append(x.astype(int))
	values.append(y.astype(int))
	values = np.transpose(values)
	if x.size==0: values=[point1]
	return values


data=[]
f = open(args.grid)
for i in f.readlines()[9:]:
    if len(i.strip()) ==0:
        pass
    else:data.append(i)
f.close()

previous_angle = float(data[0].split()[1])
local,arr=[],[]
for row in data:
    angle = float(row.split()[1])
    if angle == previous_angle:
        local.append(float(row.split()[2]))
    else:
        arr.append(local)
        previous_angle=angle
        local=[]
        local.append(float(row.split()[2]))

frames = [] 
f = open(args.frames)
for i in f.readlines():
    line=i.split(",")
    frames.append([float(line[1]),float(line[2])])
arr =np.array(arr)* .239

appendedFrames=[]
for i in range(len(frames)-1):
	point1 = np.array([int(frames[i][1]),int(frames[i][0])])
	point2 = np.array([int(frames[i+1][1]),int(frames[i+1][0])])
	newFrames = make_line(point1,point2)
	for frame in newFrames:
		appendedFrames.append(frame)

i = len(frames)-1
final_frame = np.array([int(frames[i][1]),int(frames[i][0])])
appendedFrames.append(final_frame)

arrFrameVal = []
initPoint = frames[0]
print(initPoint)
min = arr[int(initPoint[1]),int(initPoint[0])]
arr=arr-min

print(appendedFrames)
for frame in appendedFrames: 
    arrFrameVal.append(-arr[int(frame[0]),int(frame[1])])

x = np.arange(0,len(arrFrameVal),1)

fig, graph1 = plt.subplots() 
plt.scatter(x,arrFrameVal,marker='.',color='black')
labels_new=[',','initial','','','','','','final']
graph1.set_xticklabels(labels_new)
plt.ylabel('kcal/mol')
plt.xlabel('Reaction Coordinate')
plt.title('1D Path')
plt.savefig('1D-Path.png')

f = open("frames-path-all.txt","w+")
for frame in appendedFrames:
    f.write(str(frame[1])+','+str(frame[0]))
    f.write('\n')
f.close()