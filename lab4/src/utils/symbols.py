
import utils.breaking_symbols

c_printable_character_set = {0x09, 0x0a, 0x0d, *range(0x20, 0x7e + 1), 0x85, *range(
    0xA0, 0xD7FF + 1), *range(0xE000, 0xFFFD + 1), *range(0x010000, 0x10FFFF + 1)}


def is_c_printable(char):
    return ord(char) in c_printable_character_set


def is_c_mapping_key(char):
    return char == '?'


def is_c_mapping_value(char):
    return char == ':'

def is_c_sequence_entry(char):
    return char == '-'

def is_c_collect_entry(char):
  return char == ','

def is_c_sequence_start(char):
  return char == '['

def is_c_sequence_end(char):
  return char == ']'

def is_c_comment(char):
  return char == '#'

def is_c_literal(char):
  return char == '|'

def is_c_folded(char):
  return char == '>'

def is_c_single_quote(char):
  return char == '\''

def is_c_double_quote(char):
  return char == '"'

def is_nb_char(char):
  return is_c_printable(char) and not utils.breaking_symbols.is_b_char(char)
