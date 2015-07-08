
from __future__ import absolute_import

from myhdl import *

from elink import ELink
from elink import EMeshPacket
from elink import FIFO


def elink_asic_model(elink):
    """ Model a simple ELink device (something like Epiphany)

    :param elink: Interface to the external ELink enabled device
    :return: myhdl generators

    not convertible.
    """
    assert isinstance(elink, ELink)

    # get the tx and rx links based on this logical location
    tx, rx = elink.connect('south')
    gclk = tx.instances()

    pkt_i_fifo = FIFO(depth=128)
    pkt_o_fifo = FIFO(depth=128)
    pkt_delay = [EMeshPacket() for _ in range(137)]

    @instance
    def p_rx_packets():
        """ receive packets and push onto processing FIFO """
        while True:
            yield rx.frame.posedge
            bytes = []
            yield rx.lclk.posedge
            while rx.frame:
                bytes.append(intbv(int(rx.data))[8:])
                if len(bytes) == 13:
                    pkt = EMeshPacket()
                    pkt.frombytes(bytes)
                    yield delay(1)
                    pkt_i_fifo.write(pkt)
                    #@todo: if FIFO full assert wait
                    bytes = []
                yield rx.lclk.posedge
            # @todo: if len(bytes) != 13 report error - partial packet

    nslots = len(pkt_delay)

    # @todo: simulate EMesh routing
    @instance
    def p_proc_packets():
        """ process packets """
        idelay = False
        while True:
            pkt = pkt_i_fifo.read()
            if pkt is not None and pkt.access:
                if not idelay:
                    yield delay(17)
                    idelay = True
                pkt_o_fifo.write(pkt)

            if pkt_i_fifo.is_empty():
                idelay = False
                yield pkt_i_fifo.empty.negedge

    @instance
    def p_tx_packets():
        """ transmit processed packets """
        while True:
            if not pkt_o_fifo.is_empty():
                pkt = pkt_o_fifo.read()
                bytes = pkt.tobytes()
                for bb in bytes:
                    tx.frame.next = True
                    tx.data.next = bb
                    yield tx.lclk.posedge
                # packet complete clear frame
                tx.frame.next = False

            if pkt_o_fifo.is_empty():
                yield pkt_o_fifo.empty.negedge
            else:
                yield tx.lclk.posedge

    return gclk, p_rx_packets, p_proc_packets, p_tx_packets
