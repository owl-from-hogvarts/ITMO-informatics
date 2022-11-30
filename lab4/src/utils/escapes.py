
def is_c_escape(char):
    return char == '\\'


def is_ns_esc_null(char):
    return ord(char) == 0x00


def is_ns_esc_backspace(char):
    return ord(char) == 0x08


def is_ns_horizontal_tab(char):
    return ord(char) == 0x09 or char == 't'


def is_ns_esc_linefeed(char):
    return char == 'n'


def is_ns_esc_carriage_return(char):
    return char == 'r'


def is_ns_esc_space(char):
    return ord(char) == 0x20


def is_ns_esc_double_quote(char):
    return char == '"'


def is_ns_backslash(char):
    return char == '\\'


def c_ns_escape_char(char, next):
    return (is_c_escape(char) and (is_ns_esc_null(next) or
            is_ns_esc_backspace(next) or
            is_ns_horizontal_tab(next) or
            is_ns_esc_linefeed(next) or
            is_ns_esc_carriage_return(next) or
            is_ns_esc_space(next) or
            is_ns_esc_double_quote(next) or
            is_ns_backslash(next)))
