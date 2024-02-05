from pymol import cmd
from glob import glob
import sys, os
import pandas as pd

def avg_b(selection):
  stored.tempfactor = 0
  stored.atomnumber = 0
  cmd.iterate(selection, "stored.tempfactor = stored.tempfactor + b")
  cmd.iterate(selection, "stored.atomnumber = stored.atomnumber + 1")

  plddt = stored.tempfactor / stored.atomnumber
  return plddt

ref = cmd.load('8ubh.cif','ref')
print('model\tRMSD\tpLDDT')
samples = sorted(glob('preds/*pdb'))
# loop through the files
for pdb_file in samples:
    mdl = cmd.load(pdb_file,"AF_model")
    cmd.alter("AF_model","resi=str(int(resi)+1)")
    cmd.alter("AF_model","segi='A'")

    rms = cmd.fit("AF_model and name CA and (resi 3-8 or resi 13-28 or resi 35-40 or resi 45-51 or resi 58-61 or resi 68-71 or resi 76-84)",\
      "ref and name CA and (resi 3-8 or resi 13-28 or resi 35-40 or resi 45-51 or resi 58-61 or resi 68-71 or resi 76-84)")

    plddt = avg_b('AF_model')
    print("%s\t%.3f\t%.3f" % (os.path.basename(pdb_file).replace('.pdb',''), rms, plddt))
    cmd.delete("AF_model")
