import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import matplotlib.ticker as ticker
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

parser=argparse.ArgumentParser()
parser.add_argument("-grid","--grid",help="grid file to graph")
parser.add_argument("-images","--images",help="# of intermediate images")

args=parser.parse_args()

class image(object):
    def __init__(self,position,energy,spring):
        self.position = position
        self.energy = energy
        self.spring = spring

def convert_CV2(value):
    return(int(value*100))

def convert_CV1(value):
    return(int(10*value+31.4))

def find_nearest(array,value):
    array = np.asarray(array)
    idx = (np.abs(array-value)).argmin()
    return array[idx]

def make_line(initial, final):
    m = (final[1]-initial[1])/(final[0]-initial[0])
    c = final[1]-m*final[0]
    return(m,c)

def space_line(m,c,initial,final,numImages):
    pointsMatrix = []
    lineLength = final[0]-initial[0]
    spacing = lineLength/numImages
    for i in range(int(numImages)+1):
        xnew = initial[0]+spacing*i
        ynew = xnew*m + c
        pointsMatrix.append([int(xnew),int(ynew)])
    return(pointsMatrix)

def initImageList(pointsMatrix):
    #initialize Image List with pos, energy, and 0 spring force
    imageList=[]
    for val in pointsMatrix:
        imageList.append(image(val,0,0))
    return(imageList)

def distance(v1,v2):
    return(np.linalg.norm(np.array(v2)-np.array(v1)))

def updateSpringEnergy(imageList,k):
    for i in np.arange(1,len(imageList)-1,1):
        e1 = k*(distance(imageList[i-1].position,imageList[i].position))**2
        e2 = k*(distance(imageList[i].position,imageList[i].position))**2
        imageList[i].spring = (e1+e2)/2
    return(imageList)

def updateGridEnergy(imageList,grid):
    for i in imageList:
        i.energy = grid[i.position[0],i.position[1]]
    return(imageList)

def sumEnergy(imageList):
    sum = 0
    for i in imageList: sum = sum + i.energy + i.spring
    return(sum)

def perturbPosition(imageList,delta):
    for i in imageList:
        theta = np.random.ranf()*np.pi
        dx,dy = delta*np.cos(theta),delta*np.sin(theta)
        initPos = i.position
        newPos = [int(initPos[0]+dx),int(initPos[1]+dy)]
        print(initPos,newPos)
        i.position = newPos
    return(imageList)

data=[]
f = open(args.grid)
for i in f.readlines()[9:]:
    if len(i.strip()) ==0:
        pass
    else:data.append(i)

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
arr = np.array(arr)
arr = arr.transpose()
k,delta=1,3
initial = [10,0]
final = [380,25]
arr =np.array(arr)* .239

m,c = make_line(initial, final)
pointsMatrix = space_line(m,c,initial,final,float(args.images))
initImageList = initImageList(pointsMatrix)
initImageList = updateGridEnergy(initImageList,arr)
initImageList = updateSpringEnergy(initImageList,k)

imageList = initImageList
for nn in range(1):
    initEnergy = sumEnergy(imageList)
    nextimageList = perturbPosition(imageList,delta)
    print(initImageList == nextimageList)
    nextimageList = updateGridEnergy(imageList,arr)
    nextimageList = updateSpringEnergy(imageList,arr)
    nextEnergy = sumEnergy(nextimageList)
    #if nextEnergy<initEnergy: print('yes') #imageList=nextimageList
