from __future__ import division
from pystochastic import *

proc = PyStochastic()
proc.link('A1','A1',4/9)
proc.link('A1','B1',1/9)
proc.link('A1','A2',2/9)
proc.link('A1','B2',2/9)

proc.link('A2','A1',4/9)
proc.link('A2','B1',1/9)
proc.link('A2','A2',2/9)
proc.link('A2','B2',2/9)

proc.link('B1','A1',4/9)
proc.link('B1','B1',1/9)
proc.link('B1','A2',2/9)
proc.link('B1','B2',2/9)

proc.link('B2','A1',4/9)
proc.link('B2','B1',1/9)
proc.link('B2','A2',2/9)
proc.link('B2','B2',2/9)
#proc.prt()
#proc.compute()
proc.wander({'A1':1/2, 'A2':1/2}, 10)
