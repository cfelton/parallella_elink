

import myhdl
from myhdl import Signal, ResetSignal, intbv

# @todo: all vendor primitives and interfaces will move to rhea
from elink.vendor import SERDESInterface
from elink.vendor import output_diff_buffer
from elink.vendor import input_diff_buffer
from elink.vendor import input_serdes
from elink.vendor import input_serdes_bank
from elink.vendor import output_serdes_bank


def elink_io_top(
    clock_ext, reset_ext,

    # serial interface for testing
    serial_clk_out_p, serial_clk_out_n,
    serial_dat_out_p, serial_dat_out_n,
    serial_clk_in_p, serial_clk_in_n,
    serial_dat_in_p, serial_dat_in_n,
    frame_p, frame_n,

    # UART for simple CSR
    uart_tx, uart_rx,

    # misc user IO
    led_pins, pb_pins, sw_pins
    ):
    """ Test top-level for x8 serial channels

    :param clock_ext:
    :param reset_ext:
    :param serial_clk_out_p:
    :param serial_dat_out_p:
    :param serial_clk_in_p:
    :param serial_dat_in_p:
    :param frame_p:
    :param uart_tx:
    :param uart_rx:
    :param led_pins:
    :param pb_pins:
    :param sw_pins:
    :return: myhdl generators

    """

    # list of modules (myhdl generator)
    mods = []

    # @todo: generate clocks

    # map the serial ports to the SERDES interfaces
    num_channels = len(serial_dat_out_p)
    assert num_channels == len(serial_dat_in_p)

    # the top-level conversion does not support list-of-signals
    # in this case a simple bit-vector (list-of-signals) is easier
    # to deal with than the intbv, need to convert them at this point
    seri = [Signal(bool(0)) for _ in range(num_channels)]
    sero = [Signal(bool(0)) for _ in range(num_channels)]

    mods += output_diff_buffer(sero, serial_dat_out_p, serial_dat_out_n)
    mods += input_diff_buffer(serial_dat_in_p, serial_dat_in_n, seri)

    return mods


# Default port-map for the top-level
elink_io_top.port_map = {
    'clock_ext': Signal(bool(0)),
    'reset_ext': ResetSignal(0, active=0, async=True),
    'serial_clk_out_p': Signal(bool(0)),
    'serial_clk_out_n': Signal(bool(0)),
    'serial_dat_out_p': Signal(intbv(0)[8:]),
    'serial_dat_out_n': Signal(intbv(0)[8:]),
    'serial_clk_in_p': Signal(bool(0)),
    'serial_clk_in_n': Signal(bool(0)),
    'serial_dat_in_p': Signal(intbv(0)[8:]),
    'serial_dat_in_n': Signal(intbv(0)[8:]),
    'frame_p': Signal(bool(0)),
    'frame_n': Signal(bool(0)),
    'uart_tx': Signal(bool(0)),
    'uart_rx': Signal(bool(0)),
    'led_pins': Signal(intbv(0)[4:]),
    'pb_pins': Signal(intbv(0)[4:]),
    'sw_pins': Signal(intbv(0)[4:])
}


def convert():
    myhdl.toVerilog(elink_io_top, **elink_io_top.port_map)


if __name__ == '__main__':
    convert()