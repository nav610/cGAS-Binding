import mdtraj as md

t = md.load("4k98.pdb")
top = t.topolgy()
lysCA = top.select("resSeq 409 and name CA")
serCB = top.select("resSeq 305 and name CB")
mg = top.select("name MG")
cat = top.select("resSeq 213 and name CA")
PA = top.select("resSeq 604 and name PA")
ring1 = top.select("resSeq 604 and name C12 or name C22 or name C32 or name C42 or name O42")
ring2 = top.select("resSeq 605 and name C1'1 or name C2'1 or name C3'1 or name C4'1 or name O4'1")
