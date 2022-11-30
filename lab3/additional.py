
import re

regex = re.compile(r'(?:\b(?P<letter>\w(?<![вас]))(?:\s+?(?P=letter))+)|(\b(?P<word>\w+)(?:\s+?(?P=word))+\b)', re.UNICODE | re.MULTILINE | re.IGNORECASE)

def test(input_string: str):
  found = regex.search(input_string, 0)
  while found:
    r = found.group("word") if found.group("word") else found.group("letter")
    input_string = input_string[:found.start()] + r + input_string[found.end():]
    found = regex.search(input_string, found.start() + len(r))

  return input_string


print("Довольно распространённая ошибка ошибка – это лишний повтор повтор слова слова. Смешно, не не правда ли? Не нужно портить хор хоровод.")
print(test("Довольно распространённая ошибка ошибка – это лишний повтор повтор слова слова. Смешно, не не правда ли? Не нужно портить хор хоровод."))
print()
print("Пять пять тестов? Что то это на ужас похоже. Хорошо что не десять. Десять это уже совсем много")
print(test("Пять пять тестов? Что то это на ужас похоже. Хорошо что не десять. Десять это уже совсем много"))
print()
print("Ехал Грека через реку Греку, видит Грек`а Грека - в реке рек. Сунул Грека руку в руку, рак за руку руку Греку цап - цап     цап !")
print(test("Ехал Грека через реку Греку, видит Грек`а Грека - в реке рек. Сунул Грека руку в руку, рак за руку руку Греку цап - цап     цап !"))
print()
print("Остался всего один тест один т т т тест")
print(test("Остался всего один тест один т т т тест"))
print()
print("Опа, Опа опа! А вот и последний последний пример подоспел")
print(test("Опа, Опа опа! А вот и последний последний пример подоспел"))
print()
print("В валентин валентин")
print(test("В валентин валентин"))
print()
print("А ананас")
print(test("А ананас"))
print()
print("С сервер")
print(test("С сервер"))
print()
print("П привет")
print(test("П привет"))
print()

