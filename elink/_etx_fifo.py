
from __future__ import division
from __future__ import absolute_import


from myhdl import *

from rhea import cores
from rhea.system import FIFOBus

from elink._emesh_i import EMeshPacket
#from ._fifo_i import FIFO


def etx_fifo(glbl, emesh_i, emesh_o):
    """
    """

    wide_bus_i = emesh_i.bits
    wide_bus_o = emesh_o.bits

    fifo_intf = FIFOBus(size=16, width=len(emesh_i.bits))

    # map the packet signals to the FIOF
    g_fifo = cores.fifo.fifo_async(glbl.reset, emesh_i.clock, 
                                   emesh_o.clock, fbus)


    return g_fifo
        


