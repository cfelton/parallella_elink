
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from myhdl import *

from rhea import cores
from rhea.system import FIFOBus

from . import epkt_from_bits


def emesh_fifo(reset, emesh_i, emesh_o):
    """ EMesh transmit FIFO
    """

    nbits = len(emesh_i.txwr.bits)
    fbus_wr, fbus_rd, fbus_rr = [FIFOBus(size=16, width=nbits)
                                 for _ in range(3)]

    def emesh_to_fifo(epkt, fbus):
        """ assign the EMesh inputs to the FIFO bus """
        @always_comb
        def rtl_assign():
            fbus.wdata = epkt.bits
            print(epkt)
            if epkt.access:
                #fbus.write.next = True
                fbus.wr.next = True
            else:
                #fbus.write.next = False
                fbus.wr.next = False
        return rtl_assign

    def fifo_to_emesh(fbus, epkt):
        """ assign FIFO bus to emesh output """

        # map the bit-vector to the EMeshPacket interface
        map_inst = epkt_from_bits(epkt, fbus.rdata)

        # the FIFOs work with a read acknowledge vs. a read
        # request - meaning the data is available before the
        # read and transitions to the next data after the read
        # strobe

        # @todo: there is (might be) an error here if the FIFO
        #   works in read-ack, if wait is set the same packet
        #   will be stuck on the bus, need to make sure the EMesh
        #   ignores the packet when wait is set
        @always_comb
        def rtl_read():
            if not fbus.empty and not epkt.wait:
                #fbus.read.next = True
                fbus.rd.next = True
            else:
                #fbus.read.next = False
                fbus.rd.next = False

        return map_inst, rtl_read

    # create a FIFO foreach channel: write, read, read-response
    fifo_insts = []
    for epkt, fifobus in zip((emesh_i.txwr, emesh_i.txrd, emesh_i.txrr,),
                             (fbus_wr, fbus_rd, fbus_rr,)):
        fifo_insts += [emesh_to_fifo(epkt, fifobus)]
        fifo_insts += [cores.fifo.fifo_async(reset, emesh_i.clock,
                                             emesh_o.clock, fifobus)]

    # assign the output of the FIFO
    for epkt, fifobus in zip((emesh_o.txwr, emesh_o.txrd, emesh_o.txrr,),
                             (fbus_wr, fbus_rd, fbus_rr,)):
        fifo_insts += [fifo_to_emesh(fifobus, epkt)]

    return fifo_insts

