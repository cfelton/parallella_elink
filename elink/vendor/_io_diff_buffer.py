
from myhdl import Signal, always_comb

def input_diff_buffer(in_p, in_n, sig):

    if isinstance(sig, list):
        num_channels = len(sig)

        @always_comb
        def rtl_buffer():
            for ii in range(num_channels):
                sig[ii].next = in_p[ii] and not in_n[ii]

    else:

        @always_comb
        def rtl_buffer():
            sig.next = in_p and not in_n

    return [rtl_buffer,]


def output_diff_buffer(sig, out_p, out_n):

    if isinstance(sig, list):
        num_channels = len(sig)

        @always_comb
        def rtl_buffer():
            for ii in range(num_channels):
                out_p[ii].next = sig[ii]
                out_n[ii].next = not sig[ii]

    else:

        @always_comb
        def rtl_buffer():
            out_p.next = sig
            out_n.next = not sig

    return [rtl_buffer,]
