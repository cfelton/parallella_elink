
from __future__ import division
from __future__ import print_function

from myhdl import *

from . import EMeshPacket
from . import FIFO
from . import io_serdes

def elink(elink_intf, emesh_intf):
    """ The Adapteva ELink interface
    
    Interfaces
    ----------
      elink_intf: The external link signals
      emesh_intf: The internal EMesh packet interface

    """

    # keep track of all the myhdl generators
    mod_inst = []

    # clock and reset config
    #mod_inst += ecfg_elink()

    # receiver
    #mod_inst += erx(elink, emesh_e)

    # transmitter
    #mod_inst += etx(elink, emesh_e)

    # CDC FIFO
    #mod_inst += ecfg_fifo(emesh, emesh_e)

    # Vendor specific IO SERDES
    mod_inst += io_serdes()

    return mod_inst
