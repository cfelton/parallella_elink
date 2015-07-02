
from __future__ import absolute_import

from myhdl import *

from elink import ELink


def elink_asic_model(elink):

    assert isinstance(elink, ELink)

    # get the tx and rx links based on this logical location
    tx, rx = elink.south()

    @always_comb
    def p_assign():
        # @todo: interpret the packet stream and model some of the
        #    registers.
        tx.lclk.next = rx.lclk
        tx.frame.next = rx.frame
        tx.data.next = rx.data
        rx.wr_wait.next = tx.wr_wait
        rx.rd_wait.next = tx.rd_wait

    return p_assign
