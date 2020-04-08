import numpy as np
import argparse
import matplotlib.pyplot as plt

parser= argparse.ArgumentParser()
parser.add_argument("-colvar","--colvar", help = "colvar file for reading")
args = parser.parse_args()

def closest_value(arr,value):
    idx = (np.abs(arr-value)).argmin()
    return(idx)

data = []
f = open(args.colvar)
for i in f.readlines():
    if '#' in i: pass
    else:
        line = i.split()
        data.append(np.array(line[:3]).astype(float))
f.close()

CVS= []
a = np.linspace(-3.14,3.14,61)
b = np.arange(0,5.5,.01)
a = np.round(a,2)

time = 0
for value in data:
    if (np.round(value[0],1))%200 == 0:
        time = np.around(time,2)
        CVS.append(np.array([time,closest_value(b,value[2]),closest_value(a,value[1])]))
        time = time +.2


figure=plt.figure()
for value in CVS:
    print(value)
    plt.plot(value[1],value[2],marker=".")
plt.show()


f = open("frameCVS.txt","w+")
for value in CVS:
    f.write(str(value[0]) + "," + str(int(value[1])) + "," + str(int(value[2])))
    f.write("\n")
