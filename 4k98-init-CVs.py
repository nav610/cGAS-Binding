import mdtraj as md
import numpy as np

t = md.load("4k98-init.pdb")
top = t.topology

def findXYZ(index,trajxyz):
    cords=[]
    for i in index:
        cords.append(trajxyz[i])
    return np.array(cords)

def findCOM(coordArr,massArr):
    massSum = np.sum(massArr)
    weightSum = np.sum(dotProduct(coordArr,massArr),axis=0)
    return(np.divide(weightSum,massSum))

def dotProduct(arr1,arr2):
    dotProd = []
    if len(arr1)==len(arr2):
        for i in range(len(arr1)):
            dotProd.append(arr1[i]*arr2[i])
    return(np.array(dotProd))

def findPlane(point1,point2,point3):
    vector1 = point2 - point1
    vector2 = point3 - point1
    a,b,c = np.cross(vector1,vector2)
    return(np.array([a,b,c]))

def findDihedralAngle(plane1,plane2):
    numerator = np.dot(plane1,plane2)
    denom = np.linalg.norm(plane1)*np.linalg.norm(plane2)
    return(np.arccos(numerator/denom))

lys = top.select("resSeq 409 and name CA")
ser = top.select("resSeq 305 and name CB")
catRes = top.select("name MG or resSeq 215 and name CA")
bond = top.select("resSeq 604 and name PA or resSeq 604 and name C22")
ring1 = top.select("resSeq 604 and name C12 or name C22 or name C32 or name C42 or name O42")
ring2 = top.select("resSeq 605 and name C11 or name C21 or name C31 or name C41 or name O41")

lys_mass    = np.array([12.0110])
ser_mass    = np.array([12.0110])
catRes_mass     = np.array([24.3050,24.3050,12.0110])
bond_mass       = np.array([30.9738,12.0110])
ring1_mass      = np.array([12.0110,12.0110,12.0110,12.0110,15.9994])
ring2_mass      = np.array([12.0110,12.0110,12.0110,12.0110,15.9994])


#Get XYZ coordinates for each grouping of atoms
lysXYZ      = findXYZ(lys, t.xyz[0])
serXYZ      = findXYZ(ser, t.xyz[0])
catResXYZ   = findXYZ(catRes,t.xyz[0])
bondXYZ     = findXYZ(bond, t.xyz[0])
ring1XYZ    = findXYZ(ring1, t.xyz[0])
ring2XYZ    = findXYZ(ring2, t.xyz[0])

#Get COM from coordinates for each grouping
lysCOM      = findCOM(lysXYZ, lys_mass)
serCOM      = findCOM(serXYZ, ser_mass)
catResCOM   = findCOM(catResXYZ, catRes_mass)
bondCOM     = findCOM(bondXYZ, bond_mass)
ring1COM    = findCOM(ring1XYZ, ring1_mass)
ring2COM    = findCOM(ring2XYZ, ring2_mass)

plane1  = findPlane(lysCOM,ring1COM,ring2COM)
plane2  = findPlane(ring1COM, ring2COM, serCOM)
phi     = findDihedralAngle(plane1,plane2)
d       = np.linalg.norm(catResCOM-bondCOM)
print(phi,d)
