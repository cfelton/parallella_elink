
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

        # some extra signals used for modeling and testing
        self.finished = Signal(bool(0))

    def __str__(self):
        return "{:013X}".format(int(self.bits))

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

    def assign(self, pkt):
        """ assign values of pkt.
        This can only be used for modeling and testing.
        """
        self.access.next = pkt.access
        self.write.next = pkt.write
        self.datamode.next = pkt.datamode
        self.ctrlmode.next = pkt.ctrlmode
        self.dstaddr.next = pkt.dstaddr
        self.data.next = pkt.data
        self.srcaddr.next = pkt.srcaddr

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
        self.rxrr = EMeshPacket()  # RX read response, receive read acknowledge

        self._txwr_fifo = []
        self._txrd_fifo = []
        self._txrr_fifo = []

    def write(self, dstaddr, data, datau=0):
        """

        :param dstaddr:
        :param data:
        :param srcaddr:
        :return:

        not convertible
        """
        # get a new packet
        pkt = EMeshPacket(access=True, write=True, dstaddr=dstaddr, data=data, srcaddr=datau)

        # push the packet onto the TX write FIFO
        print("  send write packet {}".format(pkt))
        self._txwr_fifo.append(pkt)

        #
        #self.txwr.access.next = True
        #self.txwr.write.next = True
        #self.txwr.data.next = data
        #self.txwr.dstaddr.next = dstaddr
        #if datau is not None:
        #    self.txwr.srcaddr.next = datau
        yield self.clock.posedge

    def read(self, dstaddr, data, srcaddr):
        """

        :param dstaddr:
        :param data:
        :param srcaddr:
        :return:

        not convertible
        """
        # sent a read packet through the txrd fifo
        # if "blocking" wait for a resposse in the txrr
        pass

    def process(self, elink):
        """ process the read and write transactions (generator)
        This will take the FIFOs and send them to the ELink interface
        passed.
        :param elink:
        :return:

        not convertible
        """

        @instance
        def ptrans():
            while True:
                if len(self._txwr_fifo) > 0:
                    pkt = self._txwr_fifo.pop(0)
                    print("  push packet to elink intf {}".format(pkt))
                    self.txwr.assign(pkt)    # update the interface to reflect this
                    yield elink.send_packet(pkt)
                # @todo the other transmit FIFOs
                yield self.clock.posedge
        return ptrans

    def route_to_fifo(self, pkt):
        """ take a freshly recieved packet from the ELink interface
        Take a freshly received packet from the ELink interface and route
        it to the correct RX fifo.
        :param pkt:
        :return:

        not convertible
        """
        # if the write bit is set pass it to RX write FIFOg
        # @todo: how to determine the other packets??
        pass


