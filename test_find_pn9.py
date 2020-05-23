from decoding import find_pn9_sequences
from utility import *


sent_data_ref_o = b"ooooooooooooooooooooooooooooooooooooooooooooooooo"
bit_str_ref = '11011100000000000010110011110111001001111100000111010011111110000101011101110010101111001011101111001111001110100001001000000111010110000000001000001111110101001000110010100010010110101010100111100100100101010011011111001001010111110111011011111010111111001001100111111101000000001010010000111111110011010001100100110001101011000011101110001011010111100110011101101011001010010010100000111001101010000111110111001100000010001010000001111001100010100100111111110110101111101001100011101100100100010111000110001110000010011011000111101000010111111111111000'

pn9_sequences = find_pn9_sequences(sent_data_ref_o, bit_str_ref)
print(pn9_sequences)
pickle_result(pn9_sequences, "pn9_sequences.pckl")
