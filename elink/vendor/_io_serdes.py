
from myhdl import Signal, intbv
from . import SERDESInterface

def _io_serdes(serdes_intf):
    """ Input and output SERDES

    :param serdes_intf:
    :return: list/tuple of myhdl generators
    """

    # locally reference the interface Signals, required for
    # the HDL template conversion (primitive instantiations)

    clock_serial = Signal(bool(0))
    serial_in = Signal(bool(0))
    serial_out = Signal(bool(0))


