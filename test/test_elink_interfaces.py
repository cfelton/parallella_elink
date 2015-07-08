
from __future__ import division
from __future__ import print_function

import os
from random import randint

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

    @always(delay(2500))
    def tbclk():
        clock.next = not clock

    def _test_stim():
        tbnorth = elink_external_model(elink, emesh)
        tbsouth = elink_asic_model(elink)

        @instance
        def tbstim():
            yield delay(1111)
            yield clock.posedge

            # send a bunch of write packets
            save_data = []
            yield emesh.write(0xDEEDA5A5, 0xDECAFBAD, 0xC0FFEE)
            save_data.append(0xDECAFBAD)
            for ii in range(10):
                addr = randint(0, 1024)
                data = randint(0, (2**32)-1)
                save_data.append(data)
                yield emesh.write(addr, data, ii)

            # the other device is a simple loopback, should receive
            # the same packets sent.
            while emesh.txwr_fifo.count > 0:
                print(emesh)
                yield delay(8000)

            while len(save_data) > 0:
                yield delay(8000)
                pkt = emesh.get_packet('wr')
                if pkt is not None:
                    assert pkt.data == save_data[0], \
                        "{} ... {:08X} != {:08X}".format(
                        pkt, int(pkt.data), save_data[0])
                    save_data.pop(0)

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