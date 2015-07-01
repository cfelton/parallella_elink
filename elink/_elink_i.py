
from __future__ import division
from __future__ import print_function

from myhdl import *

from _emesh_i import EMeshPacket

class ELinkChannel(object):
    """ RX or TX channel in an ELink interface
    """
    def __init__(self):
        # The Signals for the channel
        self.lclk = Signal(bool(0))       # interface sync clock
        self.frame = Signal(bool(0))      # valid frame/data
        self.data = Signal(intbv(0)[8:])  # byterized emesh packet data
        self.wr_wait = Signal(bool(0))    # write pushback
        self.rd_wait = Signal(bool(0))    # read pushback

        # clock rate assuming 1ps simulation step
        self.htick = 500

    def _clkgen(self):
        """ Generate the clock for this interface
        :return:
        """
        @instance
        def gclkgen():
            self.lclk.next = False
            while True:
                yield delay(self.htick)
                self.lclk.next = not self.lclk

    def instances(self):
        return self._clkgen()


class ELink(object):
    """
    The ELink interface is the external interface between devices (typically
    the Adapteva Epiphany and an FPGA.

    @todo: more description

    The Epiphany datasheet (has a description of the chip-to-chip (ELink)
    interfaces:
    http://www.adapteva.com/docs/e16g301_datasheet.pdf

    The Parallella open-hardware (oh) repository:
    https://github.com/parallella/oh/tree/master/elink
    """

    def __init__(self):
        self._tx = ELinkChannel()
        self._rx = ELinkChannel()

        # Keep track how this interface is connected, only an east-west or
        # north-south connections can be established (not both).
        # The east-west and north-south are redundant but commonly used.
        self.connections = {'east': False, 'west': False,
                            'north': False, 'south': False}

    def east(self):
        assert not self.connections['east'], "East connection exists"
        self.connection['east'] = True
        return self._tx, self._rx

    def west(self):
        assert not self.connections['west'], "West connection exists"
        self.connection['west'] = True
        return self._rx, self._tx

    def north(self):
        assert not self.connections['north'], "North connection exists"
        self.connection['north'] = True
        return self._tx, self._rx

    def south(self):
        assert not self.connections['south'], "South connection exists"
        self.connection['south'] = True
        return self._rx, self._tx

    def instances(self):
        return self.tx.instances(), self.rx.instances()

    def _send_bytes(self, bytes):
        yield self._tx.lclk.posedge
        self._tx.frame.next = True
        for ii in range(13):
            self._tx.data.next = bytes[ii]
            yield self._tx.lclk.posedge
        self._tx.frame.next = False
        yield self._tx.lclk.posedge

    def _receive_bytes(self, bytes):
        ri = 0
        while ri < 13:
            yield self._rx.lclk.posedge
            if self._rx.frame:
                bytes[ri] = int(self.data)
                ri += 1

    def tr_write(self, dstaddr, data, srcaddr=0):
        """A single ELink write transaction
        """
        packet = EMeshPacket(access=1, write=1, datamode=2,
                             dstaddr=dstaddr, data=data, srcaddr=srcaddr)
        bytes = packet.tobytes()
        yield self._send_bytes(bytes)
        bytes = [None for _ in range(13)]
        yield self._receive_bytes(bytes)
        print(bytes)

    def tr_read(self, dstaddr, data, srcaddr=0):
        """ A single ELink read transaction
        """
        packet = EMeshPacket(access=1, write=0, datamode=2,
                             dstaddr=dstaddr, data=data, srcaddr=srcaddr)
        bytes = packet.tobytes()
        yield self._send_bytes(bytes)
        bytes = [None for _ in range(13)]
        yield self._receive_bytes(bytes)
        print(bytes)

    # @todo: setup streaming transactions




