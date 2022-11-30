
def is_b_line_feed(char):
    return ord(char) == 0x0a


def is_b_carriage_return(char):
    return ord(char) == 0x0d


def is_b_char(char):
    return is_b_line_feed(char) or is_b_carriage_return(char)

