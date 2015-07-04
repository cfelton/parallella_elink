
from __future__ import absolute_import

from myhdl import *

from elink import ELink
from elink import EMeshPacket
from elink import FIFO


def elink_asic_model(elink):
    """

    :param elink:
    :return:

    not convertible
    """
    assert isinstance(elink, ELink)

    # get the tx and rx links based on this logical location
    tx, rx = elink.connect('south')

    pkt_i_fifo = FIFO(depth=128)
    pkt_o_fifo = FIFO(depth=128)
    pkt_delay = [EMeshPacket() for _ in range(137)]

    @instance
    def p_rx_packets():
        while True:
            yield rx.frame.posedge
            bytes, bcnt = [], 0
            yield rx.lclk.posedge
            while rx.frame:
                bytes.append(int(rx.data))
                if len(bytes) == 13:
                    pkt = EMeshPacket()
                    pkt.frombytes(bytes)
                    pkt_i_fifo.write(pkt)
                    #@todo: if FIFO full assert wait
                yield rx.lclk.posedge
            # @todo: if len(bytes) != 13 report error - partial packet

    nslots = len(pkt_delay)

    # @todo: simulate EMesh routing
    @instance
    def p_proc_packets():
        while True:

            pkti = EMeshPacket()
            if not pkt_i_fifo.isempty():
                pkti = pkt_i_fifo.read()

            pkto = pkt_delay[nslots-1]
            if pkto.access:
                pkt_o_fifo.write(int(pkto))

            # update the delay chain
            for ii in range(1, nslots):
                pkt_delay[ii] = pkt_delay[ii-1]
            pkt_delay[0] = pkti

            yield delay(13)

    @instance
    def p_tx_packets():
        while True:
            if not pkt_o_fifo.isempty():
                pkt = pkt_o_fifo.read()
                bytes = pkt.tobytes()
                for bb in bytes:
                    tx.frame.next = True
                    tx.data.next = bb
                    yield tx.lclk.posedge

            if pkt_o_fifo.isempty():
                yield pkt_o_fifo.empty.negedge

    return p_rx_packets, p_proc_packets, p_tx_packets
