from __future__ import division
from pystochastic import *

proc = PyStochastic()
proc.link(1,3,1/3)
proc.link(1,2,2/3)
proc.link(2,1,1/2)
proc.link(2,4,1/2)
proc.link(3,3,1)
proc.link(4,4,1)
#proc.prt()
proc.compute()
#proc.wander({1:1}, 10)
