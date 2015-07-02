
from __future__ import absolute_import

from myhdl import *

from elink import ELink
from elink import EMesh


def elink_external_model(elink, emesh):

    assert isinstance(elink, ELink)
    assert isinstance(emesh, EMesh)

    # get the tx and rx links based on this module's location
    tx, rx = elink.north()

    # get the clock generator for the interface
    g_txclk = tx.instances()

    @instance
    def g_translate():

        while True:
            if emesh.access:
                if emesh.write:
                    pass

    return g_txclk, g_translate


