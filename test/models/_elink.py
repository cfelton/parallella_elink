
from __future__ import absolute_import

from myhdl import *

from elink import ELink
from elink import EMesh


def elink_external_model(elink, emesh):

    assert isinstance(elink, ELink)
    assert isinstance(emesh, EMesh)

    # get the tx and rx links based on this module's location
    tx, rx = elink.connect('north')

    # get the clock generator for the interface
    g_txclk = tx.instances()
    g_elink = elink.process()

    @instance
    def g_translate():

        # translate the EMesh transactions to ELink transactions
        while True:
            if emesh.txwr.access:
                if emesh.txwr.write:
                    yield elink.write_packet(emesh.txwr)
                else:
                    yield elink.read_packet(emesh.txrd)

            yield emesh.clock.posedge

    return g_txclk, g_elink, g_translate


