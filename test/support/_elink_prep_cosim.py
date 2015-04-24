
from __future__ import division
from __future__ import print_function

import os
import shlex
import subprocess
import pickle

from myhdl import *
from _elink_file_list import get_reference_design_file_list
from _elink_map_ports import elink_map_ports

def prep_cosim(clock, reset, keep_alive, elink, args=None):
    """
    """
    
    print("Checking reference design and building")
    # the following creates the command file with the correct
    # path, the returns are not used by this function
    vfiles, etop, cmdfile = get_reference_design_file_list()

    # this recompiles everything again ... there is a better way to
    # do this but the compiles executes quickly, so ...
    print("Compiling testbench ...")
    tbfiles = ['tb_elink.v']
    vstr = "-D VTRACE" if args.vtrace else ""
    dstr = "{} -D VTRACE_LEVEL={} -D VTRACE_MODULE={} ".format(
           vstr, args.vtrace_level, args.vtrace_module)
    cmd = "iverilog -g2001 -o elink -f elink.cmd {} {}".format(
           dstr, " ".join(tbfiles) )
    cmd = shlex.split(cmd)
    rc = subprocess.call(cmd)
    assert rc == 0, "failed to build Verilog"

    if not os.path.exists('vcd'):
        os.makedirs('vcd')

    print("Cosimulation setup ...")
    dstr = "-lxt2 " if args.vtrace else "-none "
    cmd = "vvp -m ./myhdl.vpi elink {}".format(dstr)

    # the top-level ports were automatically extracted from 
    # the Verilog elink.v.
    ports = pickle.load(open('support/elink_ports.pkl', 'r'))
    # references the signals in the interface
    gmap = elink_map_ports(ports, elink)  
    elink_ports = elink.ports

    with open('elink_ports.txt', 'w') as fp:
        for pn, ps in elink_ports.iteritems():
            fp.write("{:28}: {} \n".format(pn, repr(ps)))

    gcosim = Cosimulation(
        cmd,
        # global clock can reset, these don't exist in the elink DUT
        clock = clock,
        reset = reset,
        keep_alive = keep_alive,
        # elink interface
        **elink_ports
        )

    return gcosim, gmap


if __name__ == '__main__':
    args = Namespace(
        build_only=True,          # build only
        vtrace=True,              # enable VCD tracing in Verilog cosim
        vtrace_level=0,           # Verilog VCD dumpvars level
        vtrace_module='tb_elink', # Verilog VCD dumpvars module to trace
    )

    prep_cosim(Signal(bool(0)), ResetSignal(0, 0, False),
               None, None, args)
