
from __future__ import division
from __future__ import print_function

from myhdl import *


class EMeshPacket(object):
    """
    @todo: description
    """
    def __init__(self, access=0, write=0, datamode=2, ctrlmode=0,
                 dstaddr=0, data=0, srcaddr=0):
        """

        :param access: Indicates a valid transaction
        :param write: Indicates a write transaction
        :param datamode: Data size (0=8b, 1=16b, 2=32b, 3=64b)
        :param ctrlmode: Various special modes for the Epiphany chip
        :param dstaddr: Address for write, read-request, or read-response
        :param data: Data for a write transaction, data for read response
        :param srcaddr: Return addres for read-request upper data for write
        :return:
        """

        # set the packet fields
        self.access = Signal(bool(access))
        self.write = Signal(bool(write))
        self.datamode = Signal(intbv(datamode)[1:])
        self.ctrlmode = Signal(intbv(ctrlmode)[4:])
        self.dstaddr = Signal(intbv(dstaddr)[32:])
        self.data = Signal(intbv(data)[32:])
        self.srcaddr = Signal(intbv(srcaddr)[32:])

        # all the above a flattened into a signal bus
        #self.bits = Signal(intbv(0)[104:])
        self.bits = ConcatSignal(self.srcaddr, self.data, self.dstaddr,
                                 self.ctrlmode, self.datamode, self.write,
                                 self.access)

    def tobytes(self):
        bytes = [intbv(0)[8:] for _ in range(13)]
        for ii in range(13):
            bytes[ii][:] = self.bits[8*ii+8:8*ii]
        return bytes

    def frombytes(self, bytes):
        self.access.next = bytes[0][0]
        self.write.next = bytes[0][1]
        self.datamode.next = bytes[0][4:2]
        self.ctrlmode.next = bytes[0][8:4]
        self.dstaddr.next = concat(*bytes[5:1])
        self.data.next = concat(*bytes[9:5])
        self.data.next = concat(*bytes[13:9])

    def clear(self):
        self.acces.next = False
        self.write.next = False
        self.datamode.next = 0
        self.ctrlmode.next = 0
        self.dstaddr.next = 0
        self.data.next = 0
        self.srcaddr.next = 0

    # remove
    #def assign(self):
    #    @always_comb
    #    def rtl_assign():
    #        self.bits.next[0] = self.access
    #        self.bits.next[1] = self.write
    #        self.bits.next[4:2] = self.datamode
    #        self.bits.next[8:4] = self.ctrlmode
    #        self.bits.next[40:8] = self.dstaddr
    #        self.bits.next[72:40] = self.data
    #        self.bits.next[104:72] = self.srcaddr
    #    return rtl_assign

    def instances(self):
        g = self.assign()
        return g


class EMesh(object):
    """
    The EMesh interface on the external ELinks is defined as having
    three EMeshPacket conduits.  These conduits
    """
    def __init__(self, clock):

        self.clock = clock         # the interface clock
        self.txwr = EMeshPacket()  # TX write, send write commands
        self.txrd = EMeshPacket()  # TX read, send read commands
        self.txrr = EMeshPacket()  # TX read response, acknowledge external read commands

        self.rxwr = EMeshPacket()  # RX write, receive external write commands
        self.rxrd = EMeshPacket()  # RX read, receive external read commands
        self.rxrr = EMeshPacket()  # RX read response, recieve read acknowledge

    def tr_write(self, dstaddr, data, datau=None):
        """

        :param dstaddr:
        :param data:
        :param srcaddr:
        :return:
        """
        self.txwr.access.next = True
        self.txwr.write.next = True
        self.txwr.data.next = data
        self.txwr.dstaddr.next = dstaddr
        if datau is not None:
            self.txwr.srcaddr.next = datau
        yield self.clock.posedge

    def tr_read(self, dstaddr, data, srcaddr):
        """

        :param dstaddr:
        :param data:
        :param srcaddr:
        :return:
        """
        pass


