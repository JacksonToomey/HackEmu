def bound_value(value):
    if isinstance(value, str):
        value = binary_string_to_int(value)
    if value > 32767 or value < -32768:
        value = value + 32768
        value = value % 65536
        value = value - 32768
    return value


def binary_string_to_int(value):
    hex_string = hex(int(value, 2))
    hex_string = hex_string[2:]
    if len(hex_string) > 4:
        hex_string = hex_string[-4:]

    return int(hex_string, 16)


def match_bitmask(test, mask):
    return (test & mask) == mask
