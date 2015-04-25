
from __future__ import division
from __future__ import print_function

from myhdl import *

class EMesh(object):
    def __init__(self, name, packet_width=104):
        self.name = name
        self.access = Signal(bool(0))
        self.packet = Signal(intbv(0)[packet_width:])
        self.wait = Signal(bool(0))

    def monitor(self):
        pass


class EMesh(object):
    def __init__(self, name, address_width=32, data_width=32):
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

        @always_comb
        def assign_pakcet():
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


    def g_reset(self):
        self.access.next = True
        self.write.next = True
        self.datamode.next = 2  
        self.ctrlmode.next = 0
        self.dstaddr.next = 0x800E0000
        self.data.next = 1
        yield self.clock.posedge
        self._clear()


    def g_set_clock(self, div=2):
        self.access.next = True
        self.write.next = True
        self.datamode.next = 2
        self.ctrlmode.next = 0
        self.