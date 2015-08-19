

from myhdl import Signal, intbv

from .vendor import SERDESInterface
# @todo: need to decide if this is the best name
from .vendor import device_input_serdes
from .vendor import device_input_serdes_bank
from .vendor import device_output_serdes_bank

def elink_io_top(
    clock_ext, reset_ext,

    # serial interface for testing
    serial_clk_out_p, serial_dat_out_p,
    serial_clk_in_p, serial_dat_in_p, frame_p,

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

    # @todo: generate clocks

    # map the serial ports to the SERDES interfaces
    num_channels = len(serial_dat_out_p)
    assert num_channels == len(serial_dat_in_p)

    # the top-level conversion does not support list-of-signals
    # in this case a simple bit-vector (list-of-signals) is easier
    # to deal with than the intbv, need to convert them at this point

