
from myhdl import *

class ELinkChannel(object):
    def __init__(self, name):
        self.name = name

        # clocks for the channel
        self.lclk = Signal(bool(0))
        self.lclk90 = Signal(bool(0))
        self.lclk_div4 = Signal(bool(0))
        self.ref_clk = Signal(bool(0))

        self.frame = Signal(bool(0))
        self.data = Signal(intbv(0)[8:])
        self.wr_wait = Signal(bool(0))
        self.rd_wait = Signal(bool(0))
