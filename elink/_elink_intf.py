
from myhdl import *

from _elink_channel_intf import ELinkChannel
from _emesh_intf import EMesh

# @todo: This is the Cosimulation Interface, it needs to be renamed
#    and possibly moved to the test support directory.  This interface
#    is specific to the Verilog implementation.
class ELink(object):
    name = ''

    def __init__(self):
        # as of 03-Jun-2015 the elink interface has been changing quite
        # a bit.  Hopefully the following is close to the final ...
        self.reset = Signal(bool(0))     # POR reset
        self.sys_clk = Signal(bool(0))   # system clock for FIFOs only

        # data in channel
        self.tx = ELinkChannel('tx')     # transmit channel to external device
        self.rx = ELinkChannel('rx')     # receive channel from external device

        # internal system interface
        self.rxwr = EMesh('rxwr')        # master write (from RX)
        self.rxrd = EMesh('rxrd')        # master read request (from RX)
        self.rxrr = EMesh('rxrr')        # slave read reqsponse (from RX)

        self.txwr = EMesh('txwr')        # slave write (to TX)
        self.txrd = EMesh('txrd')        # slave read request (to TX)
        self.txrr = EMesh('txrr')        # master read response (to TX)

        self.rxwr.set_clock(self.sys_clk)
        self.rxrd.set_clock(self.sys_clk)
        self.rxrr.set_clock(self.sys_clk)

        self.txwr.set_clock(self.sys_clk)
        self.txrd.set_clock(self.sys_clk)
        self.txrr.set_clock(self.sys_clk)

        # various interface / control signals
        self.chipid = Signal(intbv(0)[12:])
        self.en = Signal(bool(1))
        self.mailbox_full = Signal(bool(0))
        self.mailbox_not_empty = Signal(bool(0))
        self.timeout = Signal(bool(0))

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
                # @todo: make the clocks more variable, determine which is async
                #        to each other and use random values (save the random values)
                if (cnt % SYSHCYC) == 0:
                    self.sys_clk.next = not self.sys_clk
                    self.tx.lclk_div4.next = not self.tx.lclk_div4
                    self.rx.lclk_div4.next = not self.rx.lclk_div4
                if (cnt % LCLKHCYC) == 0:
                    self.tx.lclk.next = not self.tx.lclk
                    self.rx.lclk.next = not self.rx.lclk
                    self.rx.ref_clk.next = not self.rx.ref_clk
                if (cnt % LCLKHCYC) == LCLK90DEG:
                    self.tx.lclk90.next = not self.tx.lclk90

        return gclkgen

    def get_gens(self):

        # clock generation for the interface
        gclk = self.clkgen()

        # packet assignments
        gpkt = [self.rxwr.m_packet(), self.rxrd.m_packet(), self.rxrr.m_packet(),
                self.txwr.m_packet(), self.txrd.m_packet(), self.txrr.m_packet()]

        # @todo: packet monitors

        return gclk, gpkt

    def loopback(self):

        @always_comb
        def assign():
            #self.rx.lclk.next = self.tx.lclk
            self.rx.frame.next = self.tx.frame
            self.rx.data.next = self.tx.data
            self.rx.wr_wait.next = self.tx.wr_wait
            self.rx.rd_wait.next = self.tx.rd_wait

        return assign
