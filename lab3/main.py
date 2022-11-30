# ;<{P

import re

smile_input = re.escape(input("Введите смайлик: "))

smile = smile_input if len(smile_input) > 0 else r';<{P' 

def test(s: str):
  return len(re.findall(smile, s))

s = input("Введите сроку для проверки: ")

if (len(s) > 0):
  print(test(s))
else: 
  print(test(";<{P;<{P;<{P")) # 3
  print(test("На мне кодовый замок! Какой же пароль? ... ;<{P")) # 1
  print(test(";<{pP")) # 0
  print(test(";<<{P;;<{P")) # 1
  print(test("ajkhdfkasdjdfl;kkj ;<{Pakldjf ;<{Print")) # 2
