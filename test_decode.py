from utility import *
from decoding import *

# demodulated data
bit_str_rec_msg = "110100010010111000001010110011000011110011000001110110001111011001000001011010011011110010111001110011110010011100001111000001110100000000101100001010011110111110010111"



filename = "pn9_sequences.pckl"
pn9 = unpickle_result(filename)
print("PN9 sequences: ", pn9)

decoded_message_hex, decoded_message_ascii = decode(bit_str_rec_msg, pn9)
print("decoded message hex: ", decoded_message_hex)
print("decoded message ascii: ", decoded_message_ascii)

