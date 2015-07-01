
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
        self._bits = intbv(0)[104:]
        # set the packet fields
        self.access = access
        self.write = write
        self.datamode = datamode
        self.ctrlmode = ctrlmode
        self.dstaddr = dstaddr
        self.data = data
        self.srcaddr = srcaddr

    @property
    def access(self):
        return self._bits[0]

    @access.setter
    def access(self, val):
        self._bits[0] = val

    @property
    def write(self):
        return self._bits[1]

    @write.setter
    def write(self, val):
        self._bits[1] = val

    @property
    def datamode(self):
        return self._bits[4:2]

    @datamode.setter
    def datamode(self, val):
        self._bits[4:2] = val

    @property
    def ctrlmode(self):
        return self._bits[8:4]

    @ctrlmode.setter
    def ctrlmode(self, val):
        self._bits[8:4] = val

    @property
    def dstaddr(self):
        return self._bits[40:8]

    @dstaddr.setter
    def dstaddr(self, val):
        self._bits[40:8] = val

    @property
    def data(self):
        return self._bits[72:40]

    @data.setter
    def data(self, val):
        self._bits[72:40] = val

    @property
    def srcaddr(self):
        return self._bits[104:72]

    @srcaddr.setter
    def srcaddr(self, val):
        self._bits[104:72] = val

    def tobytes(self):
        bytes = [intbv(0)[8:] for _ in range(13)]
        for ii in range(13):
            bytes[ii][:] = self._bits[8*ii+8:8*ii]
        return bytes


class EMesh(object):
    """
    @todo: description
    """
    def __init__(self):
        self.txwr = Signal(intbv(0)[104:])
        self.txrd = Signal(intbv(0)[104:])
        self.txrr = Signal(intbv(0)[104:])

        self.rxwr = Signal(intbv(0)[104:])
        self.rxrd = Signal(intbv(0)[104:])
        self.rxrr = Signal(intbv(0)[104:])

        self.txrd_pkt = EMeshPacket()
        self.txwr_pkt.assign(self.txwr)

    def tr_write(self, dstaddr, data, srcaddr):
        pass

    def tr_read(self, dstaddr, data, srcaddr):
        pass


