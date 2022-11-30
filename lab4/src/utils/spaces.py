
import utils.symbols

def is_s_space(char):
  return ord(char) == 0x20

def is_s_tab(char):
  return ord(char) == 0x09

def is_s_white(char):
  return is_s_space(char) or is_s_tab(char) 

def is_ns_char(char):
  return utils.symbols.is_nb_char(char) and not is_s_white(char)