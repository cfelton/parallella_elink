
from __future__ import print_function

import re
import difflib

from myhdl import *


def _search_signals(name, stype, intf):
    """ Given a port name and signal type find a match in the inteface.

    :param name: name of the port
    :param stype: the port signal type
    :param intf: the interface to search for matching signal
    :return:
    """
    sig = None
    mm = 'none'

    sub = intf.name

    # sub-interface match
    mp = {k: v for k, v in vars(intf).items()
          if re.match('.*{}.*{}.*_p'.format(sub, k), name)}

    # signal match
    ms = {k: v for k, v in vars(intf).items()
          if re.match('.*{}.*{}.*'.format(sub, k), name)}

    if len(mp) > 0:
        assert len(mp) == 1, "too many {}".format(mp)
        nm = mp.keys()[0]
        sig = mp[nm]
        mm = '.'.join((sub, nm,))
    elif len(ms) > 0:
        # @todo: loop through the matches and find the correct match ...
        #assert len(ms) == 1, "too many {}".format(ms)
        if len(ms) > 1:
            # @todo: need a more robust way to match signals, this works
            #        for now but ...
            subname = name.split('_')[-1]
            names = [nm for nm, ss in ms.iteritems()]
            bm = difflib.get_close_matches(subname, names)[0]
        else:
            bm = ms.keys()[0]
        sig = ms[bm]
        mm = '.'.join((sub, bm,))

    if sig is None:
        pass
    elif not isinstance(sig, SignalType):
        sig = None
        mm = 'none'

    return sig, mm


def elink_map_ports(ports, elink):
    """ Map the extracted raw IO (top-level ports).
    This function will map the extracted top-level IO (ports) from
    the reference Verilog to the ELink interface
    """
    portmap = {}
    eports = {}

    with open('elink_ports.txt', 'w') as fp:
        for name, stype in ports.iteritems():
                    
            sig = None
            mm = 'none'
            
            if not ('_n' in name[-2:]):
                # @todo: add AXI Master and AXI Slave
                for intf in (elink, elink.tx, elink.rx,):
                    sig, mm = _search_signals(name, stype, intf)
                    if sig is not None:
                        break  # found a signal break from the search
        
            # if the signal was found above create a reference to it
            # if not create a stub signal
            if sig is None:
                sig = Signal(stype)
                
            if eports.has_key(name):
                raise StandardError('')

            eports[name] = sig
            portmap[name] = mm
            fp.write("{:28}: {:20} --> {}\n".format(name, repr(sig), mm))

    # attach the ports to the elink interface
    elink.ports = eports

    # @todo: drive the *_n signals
    # handle all the *_n diff signals here (small number)
    dummy = Signal(bool(0))

    @always_comb
    def rtl_invert():
        dummy.next = elink.reset
    # end todo ~~~~~
        
    return rtl_invert
