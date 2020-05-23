def convert_str_to_dec(bit_str):
    """
    slice string like "1101110000" and convert each group of 8 bits into the corresponding decimal value
    """
    data_dec = []
    for i in range(0, len(bit_str), 8):
        tmp_st = bit_str[i: i + 8]
        tmp_dec = int(tmp_st, 2)
        data_dec.append(tmp_dec)
    return data_dec


def find_pn9_sequences(sent_data, received_bits):
    """
    sent_data: known sent data(for instance b"oooo"),
    received_bits: correspondent received demodulated bit string "1101110000000000001011001111011...10"
    """
    received_dec = convert_str_to_dec(received_bits)
    pn = []
    for i in range(len(sent_data)):
        tmp_sent_data = hex(sent_data[i])
        tmp_received = hex(received_dec[i])
        tmp_pn = hex(int(tmp_sent_data, 16) ^ int(tmp_received, 16))    # XOR
        pn.append(tmp_pn)
    return pn


def decode(bit_str_rec, pn9_sequences):
    decode_msg = []
    decode_msg_ascii = []
    for i in range(len(pn9_sequences)):
        data_rec_dec = convert_str_to_dec(bit_str_rec)
        tmp_byte_msg = None
        tmp_decoded_msg = None
        try:
            tmp_decoded_msg = hex(int(pn9_sequences[i], 16) ^ int(data_rec_dec[i]))
            tmp_byte_msg = bytes.fromhex(tmp_decoded_msg[2:])
            tmp_ascii_msg = tmp_byte_msg.decode("ASCII")
            decode_msg_ascii.append(tmp_ascii_msg)

        except:
            decode_msg_ascii.append(tmp_byte_msg)

        decode_msg.append(tmp_decoded_msg)

    return decode_msg, decode_msg_ascii




