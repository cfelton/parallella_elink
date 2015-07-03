
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
    # use the elink process to drive the signals
    g_elink = elink.process()
    g_emesh = emesh.process(elink)

    return g_txclk, g_elink, g_emesh


