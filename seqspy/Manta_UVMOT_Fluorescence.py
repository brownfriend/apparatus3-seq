"""Make sure the report file given by 
   (L:/data/app3/Savedir)report(L:/data/app3/RunNumber).INI 
   exists otherwise this code won't compile. 
"""
__author__ = "Pedro M Duarte"

import sys
import os
sys.path.append( os.path.split(os.path.dirname(os.path.realpath(__file__)))[0] )
import seqconf
for p in seqconf.import_paths():
	print "...adding path " + p
	sys.path.append(p)


import time
t0=time.time()

import sys, math
 
 
 
import seq, wfm, gen, uvmot, manta
report=gen.getreport()

#PARAMETERS
stepsize = float(report['SEQ']['stepsize'])
tof      = float(report['MANTA']['tof'])
texp     = float(report['MANTA']['exp'])
noatoms  = float(report['MANTA']['noatoms'])


#Use MOT beams for fluorescence imaging
probe = 'motswitch'

#SEQUENCE

s=seq.sequence(stepsize)
s=gen.initial(s)

s.wait(20.0)


#LoadRamps refers to everything done up to loading the optical trap
#Edit loadtrap.py to change any of this
s, duration = uvmot.run(s,'MANTA')


#RELEASE FROM MOT
s.digichg('motswitch',0) 
s.digichg('uvshutter',0)
s.digichg('field',0)

s.wait(tof)

#PICTURE OF ATOMS
s=manta.MantaPicture(s, texp, probe, 1)
s.wait(noatoms)
#PICTURE OF BACKGROUND
s=manta.MantaPicture(s, texp, probe, 1)
s.wait(noatoms)
#REFERENCE #1
s=manta.MantaPicture(s, texp, probe, 0)
s.wait(noatoms)
#REFERENCE #2
s=manta.MantaPicture(s, texp, probe, 0)
s.wait(noatoms)


s.wait(2.0)
s=gen.shutdown(s)
import seqconf
s.save( seqconf.seqtxtout() )
s.clear_disk()
        
print '...Compilation = %.2f seconds\n' % (time.time()-t0)
