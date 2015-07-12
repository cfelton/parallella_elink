
from __future__ import division
from __future__ import print_function

from myhdl import *

from ._emesh_i import EMeshPacket
from ._fifo_i import FIFO

def elink(elink_intf, emesh_intf):
    """ The Adapteva ELink interface
    
    Interfaces
    ----------
      elink_intf: The external link signals
      emesh_intf: The internal EMesh packet interface

    """
    
    # clock and reset config
    g_ecfg = ecfg_elink()

    # receiver
    g_erx = erx(elink, emesh_e)

    # transmitter
    g_etx = etx(elink, emesh_e)

    # CDC FIFO
    g_fifo = ecfg_fifo(emesh, emesh_e)
