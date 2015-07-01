
from __future__ import division
from __future__ import print_function

from myhdl import *

from elink import ELink   # ELink interface
from elink import EMesh   # EMesh interface

# a simple model of a device with an ELink interface
from models import elink_asic_model

# a simple model


def test_elink_interfaces():
    """

    :return:
    """

    # create the interfaces
    elink = ELink()    # links the two components (models)
    emesh = EMesh()    # interface into the Elink external component


    def _test_stim():
        tbnorth = elink_external_model(elink, emesh)
        tbsouth = elink_asic_model(elink)

        @instance
        def tbstim():
            pass

        return tbnorth, tbsouth, tbstim

