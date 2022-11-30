
import re

dist = int(input("Distance: "))
letters = input("Letters one by one spaced: ").split()

letters_str = "".join(letters)

r = ""

for i, letter in enumerate(letters):
  between = ""
  if i != len(letters) - 1:
    between = rf"(?:\w(?<![{letters_str}])){'{' + str(dist) + '}'}"
  r += letter + between

print(r)
regex = re.compile(r, re.IGNORECASE | re.MULTILINE | re.UNICODE)
print(regex.search("КоРмА"))
print(regex.search("КоРкА"))
print(regex.search("КоРчмА"))


