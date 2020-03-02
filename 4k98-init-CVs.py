import mdtraj as md
import numpy as np

t = md.load("4k98.pdb")
top = t.topology

anchors = top.select("resSeq 409 and name CA or resSeq 305 and name CB")
catRes = top.select("name MG or resSeq215 and name CA")
PA = top.select("resSeq 604 and name PA")
ring1 = top.select("resSeq 604 and name C12 or name C22 or name C32 or name C42 or name O42")
ring2 = top.select("resSeq 605 and name C1'1 or name C2'1 or name C3'1 or name C4'1 or name O4'1")

anchors_mass = np.array([12.0110,12.0110])
catRes_mass = np.array([24.3050,24.3050,12.0110])
ring1_mass = np.array([12.0110,12.0110,12.0110,12.0110,15.9994])
ring2_mass = np.array()[12.0110,12.0110,12.0110,12.0110,15.9994])


def findXYZ(index,trajxyz):
    cords=[]
    for i in index:
        coords.append(trajxyz[i])
    return np.array(cords)

def findCOM(massArr,coordArr):
    return(np.array(massArr,coordArr)/massArr)
