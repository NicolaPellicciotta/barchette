from tpp import *
from slm import *
slm=Modulator()
traps=holo.trap(-10,10,0)
h=holo.holo(traps,10,isRand=True)
slm.show(h)
