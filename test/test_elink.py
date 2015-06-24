from __future__ import division
from __future__ import print_function

import sys
import os
import random
import datetime
import argparse
from argparse import Namespace

from myhdl import *

from elink import ELink
from elink import EMesh
from support import prep_cosim

def run_testbench(args):
    
    clock = Signal(bool(0))
    reset = ResetSignal(1, active=1, async=True)
    keep_alive = Signal(bool(0))

    # Interface to the parallella/epiphany: elink
    #elinkm = ELink()     # interface to the MyHDL implementation 
    elinkv = ELink()       # interface to the Verilog implementation

    # Verilog reference design Cosimulation
    #tbdut = m_elink(glbl, elinkm)
    tbdutv = prep_cosim(clock, reset, keep_alive, elinkv, args=args)

    # clock generators, assumes 1 ps simulation timestep
    @always(delay(10000))
    def tbclk():
        clock.next = not clock

    def _test():

        # interface to the MyHDL implementation
        tbintfm = elinkv.get_gens()
        tbloopm = elinkv.loopback()

        # interface to the Verilog implementation
        tbintfv = elinkv.get_gens()
        tbloopv = elinkv.loopback()

        def pulse_reset():
            reset.next = reset.active
            elinkv.reset.next = False
            yield elinkv.sys_clk.posedge
            elinkv.reset.next = True
            yield elinkv.sys_clk.posedge
            yield delay(11113)
            reset.next = not reset.active
            elinkv.reset.next = False
            yield delay(100)
            yield clock.posedge

        @instance
        def tbstim():
            print("start simulation ...")
            
            yield pulse_reset()
            
            for ii in range(100):
                yield delay(1000)

            yield elinkv.txwr.g_nop()
            yield elinkv.txwr.g_set_clock(div=1)
            yield elinkv.txwr.g_nop()

            for ii in range(100):
                yield delay(1000)

            print("end simulation")
            raise StopSimulation

        toggle_when_alive = Signal(bool(0))

        @always(delay(1))
        def tbmon():
            if keep_alive:
                toggle_when_alive.next = not toggle_when_alive

        return tbclk, tbintfm, tbloopm, tbintfv, tbloopv, tbstim, tbmon

    if args.trace:
        traceSignals.name = 'vcd/_test_elink'
        traceSignals.timescale = '1ps'
        fn = traceSignals.name + '.vcd'
        if os.path.isfile(fn):
            os.remove(fn)
        gt = traceSignals(_test)
    else:
        gt = _test()

    # run the simulation
    Simulation((gt, tbdutv,)).run()


def test_elink():
    
    # setup arguments for the test
    # @todo: replace with command-line arguments
    args = argparse.Namespace(
        trace=True,
        vtrace=True,
        vtrace_level=0,
        vtrace_module='tb_elink',
    )
            
    run_testbench(args)


if __name__ == '__main__':
    test_elink()