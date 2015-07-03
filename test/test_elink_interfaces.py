
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

    @always(delay(5000))
    def tbclk():
        clock.next = not clock

    def _test_stim():
        tbnorth = elink_external_model(elink, emesh)
        tbsouth = elink_asic_model(elink)

        @instance
        def tbstim():
            yield delay(1111)
            yield clock.posedge
            yield emesh.write(0x0000A5A5, 0xDECAFBAD)
            yield delay(100)

            for ii in range(27):
                yield clock.posedge

            raise StopSimulation

        return tbclk, tbnorth, tbsouth, tbstim

    traceSignals.timescale = '1ps'
    traceSignals.name = 'vcd/_test_interfaces'
    if os.path.isfile(traceSignals.name+'.vcd'):
        os.remove(traceSignals.name+'.vcd')
    g = traceSignals(_test_stim)
    #g = _test_stim()
    Simulation(g).run()


if __name__ == '__main__':
    test_elink_interfaces()