import symbols

def is_c_indicator(char):
  for name, val in symbols.__dict__.iteritems(): # iterate through every module's attributes
    if callable(val): # check if callable (normally functions)
        if val(char):
          return True
  
  return False