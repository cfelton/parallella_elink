
from myhdl import *

# @todo: this object needs to be shared between the MyHDL version
#    and the Cosimulation version.
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


class ELink(object):
    name = ''

    def __init__(self):
        # as of 03-Jun-2015 the elink interface has been changing quite
        # a bit.  Hopefully the following is close to the final ...
        self.reset = Signal(bool(0))     # POR reset
        self.sys_clk = Signal(bool(0))   # system clock for FIFOs only

        # data in channel
        self.tx = ELinkChannel('tx')
        self.rx = ELinkChannel('rx')

        # AXI master

        # AXI slave

        # map the raw IO from `elink.v` to the interface
        self.ports = {}        

    def clkgen(self):
        """ Generate the clocks for the elink design
        :return:
        """
        """
        :return:
        """

        # sys_clk and div4 set to 50MHz
        # faster clocks set to 200MHz (sim tick == ps)
        CLKINC = 100      # sim step increment
        CLKMOD = 20000    # when to wrap the clock counter
        SYSHCYC = 20000   # number of ticks in `sys_clk` half cycle
        LCLKHCYC = 5000   # number of ticks in `lclk` half cycle
        LCLK90DEG = 2500  # number of ticks in `lclk` 90 degree offset

        @instance
        def gclkgen():
            self.sys_clk.next = False

            cnt = 0
            while True:
                yield delay(CLKINC)
                cnt = (cnt + CLKINC) % CLKMOD
                if (cnt % SYSHCYC) == 0:
                    self.sys_clk.next = not self.sys_clk
                    self.tx.lclk_div4.next = not self.tx.lclk_div4
                    self.rx.lclk_div4.next = not self.rx.lclk_div4
                elif (cnt % LCLKHCYC) == 0:
                    self.tx.lclk.next = not self.tx.lclk
                    self.rx.lclk.next = not self.rx.lclk
                elif (cnt % LCLKHCYC) == LCLK90DEG:
                    self.tx.lclk90 = not self.tx.lclk90

        return gclkgen

    def get_gens(self):
        
        gclk = self.clkgen()

        return instances()

    def loopback(self):

        @always_comb
        def assign():
            #self.rx.lclk.next = self.tx.lclk
            self.rx.frame.next = self.tx.frame
            self.rx.data.next = self.tx.data
            self.rx.wr_wait.next = self.tx.wr_wait
            self.rx.rd_wait.next = self.tx.rd_wait

        return assign
