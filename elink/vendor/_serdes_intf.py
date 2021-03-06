
from myhdl import Signal, intbv, always_comb
from . import Vendor

class SERDESInterface(Vendor):
    def __init__(self, clock_serial, clock_parallel=None, number_of_bits=8):
        """

        :param clock_serial: serial clock
        :param clock_parallel:
        :param number_of_bits: number of bits to convert to to parallel/serial

        """
        self.number_of_bits = number_of_bits
        nbits = number_of_bits
        self.clock_serial = clock_serial
        self.clock_parallel = clock_parallel

        # serial bits input/output
        self.serial = Signal(bool(0))

        # parallel data
        self.data = Signal(intbv(0)[nbits:])

    def input_buffer(self, seri_p, seri_n):
        @always_comb
        def rtl():
            self.serial.next = seri_p and not seri_n
        return rtl,

    def output_buffer(self, sero_p, sero_n):
        @always_comb
        def rtl():
            sero_p.next = self.serial
            sero_n.next = not self.serial
        return rtl,

    def get_signals(self):
        return (self.clock_serial, self.clock_parallel, self.data,)
