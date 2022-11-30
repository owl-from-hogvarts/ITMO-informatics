
import symbols


def is_c_flow_indicator(char):
    return symbols.is_c_collect_entry(char) or symbols.is_c_sequence_start(char) or symbols.is_c_sequence_end(char)
