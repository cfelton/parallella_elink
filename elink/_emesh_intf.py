
from __future__ import division
from __future__ import print_function

from myhdl import *


class EMesh(object):
    """
     PACKET FIELD  | BITS    | DESCRIPTION
    --------------|---------|----------
    access        | [0]     | Indicates a valid transaction
    write         | [1]     | Indicates a write transaction
    datamode[1:0] | [3:2]   | Datasize (00=8b,01=16b,10=32b,11=64b)
    ctrlmode[3:0] | [7:4]   | Various special modes for the Epiphany chip
    dstraddr[31:0]| [39:8]  | Address for write, read-request, or
                              read-responses
    data[31:0]    | [71:40] | Data for write transaction, data for
                              read response
    srcaddr[31:0] | [103:72]| Return address for read-request, upper
                              data for write
    """
    def __init__(self, name='', address_width=32, data_width=32):
        self.name = name

        packet_width = address_width*2 + data_width + 8
        self.address_width = address_width
        self.data_width = data_width
        self.packet_width = packet_width

        self.packet = Signal(intbv(0)[packet_width:0])
        self.access = Signal(bool(0))
        self.write = Signal(bool(0))
        self.wait = Signal(bool(0))
        
        self.datamode = Signal(intbv(0)[2:])
        self.ctrlmode = Signal(intbv(0)[4:])
        self.dstaddr = Signal(intbv(0)[address_width:])
        self.data = Signal(intbv(0)[data_width:])
        self.scraddr = Signal(intbv(0)[address_width:])
        self.clock = None

    def set_clock(self, clock):
        self.clock = clock

    def m_packet(self):

        aw = self.address_width
        dw = self.data_width
        pw = self.packet_width

        # create the
        @always_comb
        def assign_packet():
            self.packet.next[0] = self.access
            self.packet.next[1] = self.write
            self.packet.next[4:2] = self.datamode
            self.packet.next[8:4] = self.ctrlmode
            b = 8
            self.packet.next[aw+b:b] = self.dstaddr
            b = b + aw
            self.packet.next[dw+b:b] = self.data
            b = b + dw
            self.packet.next[aw+b:b] = self.srcaddr

        return assign_packet

    def m_monitor(self):
        pass

    def _clear(self):
        self.access.next = False
        self.write.next = False
        self.datamode.next = 0
        self.ctrlmode.next = 0

    def g_assert_reset(self):
        self.access.next = True
        self.write.next = True
        self.datamode.next = 2  
        self.ctrlmode.next = 0
        self.dstaddr.next = 0x800E0000
        self.data.next = 1
        yield self.clock.posedge
        self._clear()

    def g_deassert_reset(self):
        pass

    def g_stop_clock(self):
        pass

    def g_start_clock(self):
        pass

    def g_set_clock(self, div=1):
        self.access.next = True
        self.write.next = True
        self.datamode.next = 2
        self.ctrlmode.next = 0
        self.dstaddr.next = 0x800E0004
        divval = {1: 0x001, 2: 0x111, 4: 0x221, 8: 0x331, 16: 0x441, 
                  32: 0x551, 64: 0x661}
        self.data.next = divval[div]
        yield self.clock.posedge
        self._clear()

    def g_nop(self):
        self.access.next = True
        self.write.next = True
        self.datamode.next = 2
        self.ctrlmode.next = 0
        self.dstaddr.next = 0x80000000
        yield self.clock.posedge
        self._clear()

    def g_enable(self, enable='both'):
        """ tx, rx, or both """
        pass

    def g_write(self, srcaddr, dstaddr, val):
        self.access.next = True
        self.write.next = True
        self.datamode.next = 2
        self.ctrlmode.next = 0
        self.dstaddr.next = dstaddr
        self.data.next = val
        self.srcaddr.next = srcaddr
        yield self.clock.posedge
        set._clear()

    def g_read(self, srcaddr, dstaddr):
        self.access.next = True
        self.write.next = False
        self.datamode.next = 2
        self.ctrlmode.next = 0
        self.dstaddr.next = dstaddr
        self.data.next = 0
        self.srcaddr.next = srcaddr
        yield self.clock.posedge
        self._clear()
