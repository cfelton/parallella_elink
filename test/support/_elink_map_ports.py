
from __future__ import print_function

import re
from myhdl import *


def _search_signals(name, stype, intf):

    sig = None
    mm = 'none'

    sub = intf.name

    mp = [(k,v,) for k,v in vars(intf).items() 
          if re.match('.*{}.*{}.*_p'.format(sub, k), name)]

    ms = [(k,v,) for k,v in vars(intf).items() 
          if re.match('.*{}.*{}.*'.format(sub, k), name)]

    if len(mp) > 0:
        assert len(mp) == 1
        sig = mp[0][1]
        mm = '.'.join((sub, mp[0][0],))
    elif len(ms) > 0:
        assert len(ms) == 1
        sig = ms[0][1]
        mm = '.'.join((sub, ms[0][0],))

    if sig is None:
        pass
    elif not isinstance(sig, SignalType):
        #print('** None\'ng {} {}'.format(name, stype))
        sig = None
        mm = 'none'

    return sig, mm


def elink_map_ports(ports, elink):
    ''' Map the extracted raw IO (top-level ports).
    This function will map the extrated top-level IO (ports) from 
    the reference Verilog to the ELink interface
    '''
    portmap = {}
    eports = {}

    for name, stype in ports.iteritems():
                
        sig = None
        mm = 'none'
        
        if not ('_n' in name[-2:]):
            # @todo: add AXI Master and AXI Slave
            for intf in (elink, elink.tx, elink.rx,):
                sig, mm = _search_signals(name, stype, intf)
                if sig is not None:
                    break

        # if the signal was found above create a reference to it
        # if not create a stub signal
        if sig is None:
            sig = Signal(stype)
            
        eports[name] = sig
        portmap[name] = mm
        print("{} --> {} ".format(name, mm))


    # attach the ports to the elink interface
    elink.ports = eports

    # handle all the *_n diff signals here (small number)
    dummy = Signal(bool(0))
    @always_comb
    def rtl_invert():
        dummy.next = elink.resetb
        
    return rtl_invert
