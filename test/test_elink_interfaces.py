
from __future__ import division
from __future__ import print_function

import os

from myhdl import *

from elink import ELink   # ELink interface
from elink import EMesh   # EMesh interface

# a simple model of a device with an ELink interface
from models import elink_asic_model

# a simple model for the FPGA side
from models import elink_external_model


def test_elink_interfaces():
    """

    :return:
    """
    clock = Signal(bool(0))
    # create the interfaces
    elink = ELink()      # links the two components (models)
    emesh = EMesh(clock) # interface into the Elink external component

    @always(delay(5))
    def tbclk():
        clock.next = not clock

    def _test_stim():
        tbnorth = elink_external_model(elink, emesh)
        tbsouth = elink_asic_model(elink)

        @instance
        def tbstim():
            yield delay(100)
            yield emesh.tr_write(0x00000000, 0xDECAFBAD)
            yield delay(100)

            raise StopSimulation

        return tbclk, tbnorth, tbsouth, tbstim

    traceSignals.name = 'vcd/_test_interfaces'
    if os.path.isfile(traceSignals.name+'.vcd'):
        os.remove(traceSignals.name+'.vcd')
    g = traceSignals(_test_stim)
    Simulation(g).run()


if __name__ == '__main__':
    test_elink_interfaces()