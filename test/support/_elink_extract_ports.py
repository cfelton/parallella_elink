
from __future__ import print_function

import os
import re
from collections import OrderedDict
import pickle
import argparse
import re

import pyparsing

from myhdl import *

from _verilog_parse import parse_verilog


# this is completely ridonculous, no idea how to deal with the 
# ouptut of the verilog parser ... the following was determined 
# by trial-and-error

from _elink_file_list import REF_DESIGN_DIR

class ELinkVerilogIntf(object):
    def __init__(self, ports):
        assert isinstance(ports, dict)
        self.inputs = OrderedDict()
        self.outputs = OrderedDict()
        self.ports = OrderedDict()

        for portname, info in ports.iteritems():
            ub,lb = info['width']
            plen = ub-lb+1
            if plen == 1:
                stype = bool(0)
            else:
                stype = intbv(0)[ub+1:lb]

            self.__dict__[portname] = Signal(stype)
            # references to the signals for auto Cosimulation connection
            # @todo: Signal is currently not picklable, only save the
            #    type and wrap in signal on the import ...
            self.ports['elink_'+portname] = stype #self.__dict__[portname]

            if info['dir'] == 'input':
                self.inputs[portname] = self.__dict__[portname]
            elif info['dir'] == 'output':
                self.outputs[portname] = self.__dict__[portname]


def parse_ports(refpath=None, args=None):
    """ parse the ports from the elink refernce design
    """
    if refpath is None:
        refpath = REF_DESIGN_DIR

    fn = os.path.join(refpath, 'elink/hdl/elink.v')
    filelines = open(fn, 'r').readlines()
    filestr = ''.join(filelines)
    tokenized = parse_verilog(filestr)

    # store the ports in a dictionary
    ports = OrderedDict()
    
    mod = tokenized[0]
    for result in mod[0]:
        if isinstance(result, pyparsing.ParseResults):
            for port in result:
                # @todo: if 2001 port style, another ParseResults will exist
                ports[port[0]] = {}
        
    for result in mod[1]:
        if isinstance(result, pyparsing.ParseResults):
            if isinstance(result[0], pyparsing.ParseResults):
                pass #print("** ", result[0])
            else:
                # parameters declarations
                if 'parameter' in result[0]:
                    # @todo: get parameters
                    pass #print("[PARAM]: {}".format(result))
    
                # get ports, if not defined in the module argument list
                elif ('input' in result[0] or 'output' in result[0] or 
                      'inout' in result[0]):
                    pdir = result[0]
                    
                    # walk through declaration tokens, find name and width
                    ub,lb = None, None
                    for ii, tok in enumerate(result):
                        if not isinstance(tok, str):
                            print(type(tok), tok)
                            if isinstance(tok, pyparsing.ParseResults):
                                print(tok.getNames)
                                # @todo: see if this is a parameter
                            #else:
                            continue

                        m = re.match('[0-9]+', tok)
                        if m is not None and ub is None:
                            ub = int(m.group())
                        elif m is not None:
                            lb = int(m.group())
                        elif ':' == tok:
                            assert ub is not None, "Did not find upper range"
    
                        if ports.has_key(tok):
                            pname = tok
                            ports[pname]['dir'] = pdir
                            if ub is not None and lb is not None:
                                ports[pname]['width'] = (ub,lb,)
                            else:
                                ports[pname]['width'] = (0,0,)
    
                # check variable declarations and if they exist in the port                
                elif 'reg' in result[0] or 'wire' in result[0] or 'logic' in result[0]:
                    pass
                    
                else:
                    pass #print("<->: {}".format(result))
    
                #print(result)
    
    #for port,info in ports.iteritems():
    #    print("  {:16}: {:6}, {}".format(port, info['dir'], info['width']))

    elink = ELinkVerilogIntf(ports)
    return elink, ports


def m_elink_stub(elink):
    Nout = len(elink.outputs)
    Nin = len(elink.inputs)
    print("Number of inputs {}, Number of outputs {}".format(Nin, Nout))

    for ii, kv in enumerate(elink.outputs.iteritems()):
        name, sig = kv
        sig.driven = True
    sig = None

    diffsigs = {}
    for ii, kv in enumerate(elink.inputs.iteritems()):
        name, sig = kv
        if re.match('.*_n', name):
            neg = sig
            pos = [sig for k, v in elink.inputs.iteritems() 
                   if (name[:-2]+'_p' == k) ][0]
            diffsigs[name] = (pos, neg,)
    sig, v = None, None
    pos, neg = None, None

    keepd = Signal(intbv(0)[64:])
    keepr = Signal(intbv(0)[64:])

    @always(elink.sys_clk.posedge)
    def rtlin():
        keepd.next = 1
            
    @always(elink.sys_clk.posedge)    
    def rtlout():
        keepr.next = keepd

    #def invert(pos, neg):
    #    @always_comb
    #    def rtl():
    #        neg.next = ~pos
    #    return rtl

    # @todo: REMOVE, the following doesn't work as desired, the nets
    #    are renamed ...
    # generate the negative diff signals in the testbench inteface,
    # note this will make all *_n signals inputs to the testbench
    # which is ok
    #ginv = [None for _ in range(len(diffsigs))]
    #ii = 0
    #for name, sigs in diffsigs.iteritems():
    #    ginv[ii] = invert(sigs[0], sigs[1])
    #    ii = ii + 1

    return rtlin, rtlout #, ginv


def main(refpath, args):
    elink, ports = parse_ports(refpath, args)
        
    if args.dump_testbench:
        # convert the stub module, also creates the testbench interface.
        # The testbench interface used is a manually modified version
        # of the converted testbench.
        toVerilog(m_elink_stub, elink)

    print('pickle ports')
    pickle.dump(elink.ports, open('elink_ports.pkl', 'wb'), protocol=-1)        

    try:
        # @note: currenlty Signal cannot be pickled because the 
        #    defined __slots__ and not __getstate__, in general is 
        #    it a good idea to be able to pickel MyHDL objects?
        print('pickle elink interface')
        pickle.dump(elink, open('elink.pkl', 'wb'), protocol=-1)
    except:
        print("@E: myhdl.Signal not picklable")
        
    
if __name__ == '__main__':
    args = argparse.Namespace(
        dump_testbench=True,      # convert the stub (new testbench)
        )

    refpath = '../../parallella_oh'
    main(refpath, args)