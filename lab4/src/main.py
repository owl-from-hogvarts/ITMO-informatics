import scanner
import types

tokens = [scanner.Space, scanner.Break]
current_token = None
generator = None

output = []

def matchToken(tokens, char, position):
  for Token in tokens:
    if Token.matcher_type == 'single':
      if Token.test(char):
        token = Token(position)
        token.append(char)

        yield token
        return
    else:
      token = Token(position)
      generator = token.append(char)
      result = generator.send(None)

      while result == None:
        next_char = yield result
        result = generator.send(next_char)

      yield token
      return
      



with open("schedule.yaml") as source:
  source = source.read()

  cursor = 0

  while cursor < len(source):
    current_char = source[cursor]

    if generator:
      result = generator.send(current_char) # should be already initialized
      current_token.append(current_char)
      if result != None:
        if result:
          output.append(current_token)
        generator = None
        continue

    if current_token:
      if current_token.append(current_char):
        continue
      else:
        output.append(current_token)
        current_token = None

    generator = matchToken(tokens, current_char, cursor)
    current_token = generator.send(None)
    


for generator in output:
  print(generator.id, generator.start, generator.length)
