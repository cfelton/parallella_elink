
from __future__ import print_function

from myhdl import *

class FIFO(object):
    """
    FIFO interface and model.
    """
    def __init__(self, depth=16, width=16, clock_read=None, clock_write=None):
        self.depth = depth
        self.clock_write = clock_write
        self.clock_read = clock_read
        self.write = Signal(bool(0))            # write strobe
        self.read = Signal(bool(0))             # read strobe
        self.empty = Signal(bool(1))            # FIFO is empty
        self.full . Signal(bool(0))             # FIFO is full
        self.data_i = Signal(intbv(0)[width:])  # data input
        self.data_o = Signal(intbv(0)[width:])  # data output
        self.data_valid = Signal(bool(0))       # data out is valid

        # modeling only
        self._fifo = []

    def write(self, data):
        """ write to the FIFO (model)
        :param data: data to push onto the FIFO
        :return: None

        not convertible
        """
        if len(self._fifo) < self.depth:
            self._fifo.append(int(data))

        if len(self._fifo) >= self.depth:
            self.full.next = True
        else:
            self.full.next = False

    def read(self):
        """ read from the FIFO (model)

        :return: data read

        not convertible
        """
        data = None
        if len(self._fifo) > 0:
            data = self._fifo.pop(0)

        if len(self._fifo) == 0:
            self.empty.next = True
        else:
            self.empty.next = False

        return data

    def isempty(self):
        return len(self._fifo) == 0

    def isfull(self):
        return len(self._fifo) >= self.depth



