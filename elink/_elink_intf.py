
from myhdl import *

# @todo: this object needs to be shared between the MyHDL version
#    and the Cosimulation version.
class ELinkChannel(object):
    def __init__(self, name):
        self.name = name
        self.lclk = Signal(bool(0))
        self.frame = Signal(bool(0))
        self.data = Signal(intbv(0)[8:])
        self.wr_wait = Signal(bool(0))
        self.rd_wait = Signal(bool(0))


class ELink(object):
    name = ''

    def __init__(self):
        self.clkin = Signal(bool(0))          # clock into elink
        self.hard_reset = Signal(bool(0))     # active high-sync hardware reset
        self.clkbypass = Signal(intbv(0)[2:]) # bypass clock for elink w/o pll
        self.colid = Signal(intbv(0)[4:])     # Ephiphany colid (from elink)
        self.rowid = Signal(intbv(0)[4:])     # Ephiphany rowid (from elink)
        self.cclk = Signal(bool(0))           # Ephiphany clock (from elink)
        self.resetb = Signal(bool(0))         # Ephiphany reset (from elink)


        # data in channel
        self.tx = ELinkChannel('tx')
        self.rx = ELinkChannel('rx')

        # AXI master

        # AXI slave

        # map the raw IO from `elink.v` to the interface
        self.ports = {}        


    def get_gens(self):
        
        @always(delay(10000))
        def elink_cclk():
            self.clkin.next = not self.clkin            

        return instances()


    def m_loopback(self):

        @always_comb
        def assign():
            self.rx.lclk.next = self.tx.lclk
            self.rx.frame.next = self.tx.frame
            self.rx.data.next = self.tx.data
            self.rx.wr_wait.next = self.tx.wr_wait
            self.rx.rd_wait.next = self.tx.rd_wait

        return assign
