"""
HOLYBRO TELEMETRY RADIO
Demodulate and decode data transmitted between two Holibro telemetry radios
The data was recorded with HackRF, URH was used for demodulation and aligning of received data
This script can be used as an external program in URH for decoding data that was whitened by Si1000 with whitening sequences

bytes 1 to 8:       preamble
bytes 9 to 24:      synchronization
bytes 25 to 40:     header
bytes 41 to end:    data -> apply decoding to this data

usage:  decode_si1000_PN9_pseudo_random.py 001110010101001010101...
"""

import sys
import re

# First 49 pseudo random sequences used for data whitening before transmission by Si1000 chip (values found experimentally)
pn9_seqs = \
    ['0xb3','0x6f','0x43','0x98','0x48','0xae','0xbc','0x97','0x38','0x1d','0xd3','0xd4','0xa0','0x55','0x7d','0x68','0x37','0x6d','0x60','0xbb',      '0xe3','0xcd','0x35','0xc6','0x8b','0xfa','0x58','0xa6','0x30','0x19','0x95','0x93','0xf6','0x92','0x6f','0xcb','0x50','0xa2','0x76','0x5e',     '0xc3','0x54','0xe4','0x31','0x8','0x4','0x46','0x47','0x56']

total_header_length = 5 # bytes


def bitstream_2_bytes(bit_str):
    byte_str = []
    for i in range(0, len(bit_str)-8, 8):
        tmp = bit_str[i: i + 8]
        tmp_dec = int(bit_str[i: i + 8], 2)
        byte_str.append(tmp_dec)
    return byte_str


def get_input_data():
    data = sys.argv[1]
    pattern = r'[^0-1]'                         #regex pattern only 0 and 1 allowed
    if re.search(pattern, data):
        raise ValueError("Invalid input data: "+data)
    return data


def decode(input_data):
    input_data_bytes = bitstream_2_bytes(input_data)
    decode_len = min(len(pn9_seqs), len(input_data_bytes)-total_header_length)
    decoded_bytes = []

    for i in range(total_header_length + decode_len):
        if i < total_header_length:
            decoded_bytes.append(hex(int(input_data_bytes[i])))
        else:
            try:
                decoded_bytes.append(hex(int(pn9_seqs[i-total_header_length], 16) ^ int(input_data_bytes[i])))
            except:
                # decoding should stop, otherwise one byte is missing in the stream
                raise RuntimeError("Error when decoding byte " + str(i) + " : ") # + input_data_bytes[i])

    return decoded_bytes


def print_result_hex(hex_bytes):
    out_str = ''
    for d in hex_bytes:
        out_str += d[2:]
        #out_str += ' '
    print(out_str)


def print_result_ASCII(hex_bytes):
    out_str = ''
    for d in hex_bytes:
        try:
            out_str += d.decode("ASCII")
        except:
            out_str += 'XX'
        #out_str += ' '
    print(out_str)

def print_result_binary(hex_bytes):
    out_str = ''
    for d in hex_bytes:
        out_str += format(int(d, 16), '08b')   # format with 0b and leading zeros: '#010b'
        #out_str += ' '
    print(out_str)



if __name__ == '__main__':

    input_data = get_input_data()
    decoded_data = decode(input_data)
    #print_result_hex(decoded_data)
    #print(input_data)
    print_result_binary(decoded_data)
    #print_result_ASCII(decoded_data)



