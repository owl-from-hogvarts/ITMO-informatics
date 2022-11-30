import re
s = input("Введите номер")
regex = re.compile(r"^(?:(\+|00)\(?)?(\d{1,3})\)?\(?(?:\d{3,5})\)?\(?\d{3}-?\d{2}(-?\d{2})?\)?$", re.UNICODE | re.MULTILINE | re.IGNORECASE)

def test(input_string: str):
  found = regex.search(input_string)
  if (found): 
    return found.group()

if len(s) > 0:
  print(test(s))
else:
  print(test("89657667899"))
  print(test("+7(965)7667899"))
  print(test("77adf777adf45"))
  print(test("77(8005)5535555"))
  print(test("88005553555"))
  print(test("+71(76865)567-67-64-4"))
