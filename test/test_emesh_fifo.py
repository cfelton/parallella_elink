
from __future__ import division
from __future__ import print_function

import os
from copy import deepcopy

import myhdl
from myhdl import (Signal, ResetSignal, always, instance, delay,
                   traceSignals, Simulation,)

from elink import EMesh
from elink import emesh_fifo


def test_emesh_fifo():
    """

    :return:
    """

    clock_a, clock_b = Signal(bool(0)), Signal(bool(0))
    reset = ResetSignal(0, active=1, async=False)
    emesh_a, emesh_b = EMesh(clock_a), EMesh(clock_b)
    input_data, output_data = [], []

    @always(delay(2500))
    def tbclka():
        clock_a.next = not clock_a

    @always(delay(3000))
    def tbclkb():
        clock_b.next = not clock_b

    @always(clock_b.posedge)
    def tbmon():
        if emesh_b.txwr.access or emesh_b.txrd.access or emesh_b.txrr.access\
                :
            output_data.append(deepcopy(emesh_b))

    def _test_stim():
        print("get emesh_fifo")
        tbdut = emesh_fifo(reset, emesh_a, emesh_b)

        @instance
        def tbstim():
            print("start stim")
            yield delay(1111)
            yield clock_a.posedge

            yield emesh_a.write(0xDEEDA5A5, 0xDECAFBAD, 0xC0FFEE)
            input_data.append(deepcopy(emesh_a))
            yield emesh_b.access
            print("  fifo ouput emesh {}".format(emesh_b))

            yield(10000)
            raise myhdl.StopSimulation

        return tbclka, tbclkb, tbmon, tbdut

    print("start simulation")


    Simulation(traceSignals(_test_stim)).run()
    #Simulation(_test_stim()).run()
    #myhdl.toVerilog()


if __name__ == '__main__':
    test_emesh_fifo()