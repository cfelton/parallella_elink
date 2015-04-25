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
    elink = ELink()       # interface between FPGA <-> Epiphany
    emesh_ext = EMesh()   # ??
    emesh_dv = EMesh()    # ??

    # Verilog reference design Cosimulation
    tbdutv = prep_cosim(clock, reset, keep_alive, elink, args=args)

    # clock generators, assumes 1 ps simulation timestep
    @always(delay(10000))
    def tbclk():
        clock.next = not clock

    
    def _test():

        tbintf = elink.get_gens()
        tbloop = elink.m_loopback()

        def pulse_reset():
            reset.next = reset.active
            elink.hard_reset.next = False
            yield elink.clkin.posedge
            elink.hard_reset.next = True
            yield elink.clkin.posedge
            yield delay(11113)
            reset.next = not reset.active
            elink.hard_reset.next = False
            yield delay(100)
            yield clock.posedge


        @instance
        def tbstim():
            print("start simulation ...")
            
            yield pulse_reset()
            
            for ii in range(100):
                yield delay(1000)

            print("end simulation")
            raise StopSimulation

        toggle_when_cclk = Signal(bool(0))
        toggle_when_alive = Signal(bool(0))

        # test the auto-mapping
        cclk_p = elink.ports['elink_cclk_p']
        cclk_n = elink.ports['elink_cclk_n']
        @always(delay(1))
        def tbmon():
            if cclk_p and not cclk_n:
                toggle_when_cclk.next = not toggle_when_cclk
            if keep_alive:
                toggle_when_alive.next = not toggle_when_alive

        return tbclk, tbintf, tbloop, tbstim, tbmon


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

        