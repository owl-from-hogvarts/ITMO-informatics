import re
from scanner import Token

# Abstract
RE_FLAGS = re.UNICODE | re.IGNORECASE

def check_result(result):
    if result:
        return result.group(0)

    return ""


class Space(Token):
    def __init__(self, start, raw: str):
        super().__init__(start, raw)
        self.id = 's-space'

    @property
    def value(self):
        return len(self.raw)

    @staticmethod
    def match(start: int, string: str):
        space_regex = re.compile('^ +', RE_FLAGS)
        result = space_regex.search(string[start:])
        return check_result(result)


class LineBreak(Token):
    def __init__(self, start: int, raw: str):
        super().__init__(start, raw)
        self.id = 'b-break'

    @staticmethod
    def match(start: int, string: str):
        break_regex = re.compile(r"^(\r\n|\n|\r)", RE_FLAGS)
        result = break_regex.search(string[start:])
        return check_result(result)


class StringQuotedLiteral(Token):
    def __init__(self, start: int, raw: str):
        super().__init__(start, raw)
        self.id = 's-string-literal-quoted'

    @property
    def value(self):
        return self.raw[1:-1]

    @staticmethod
    def match(start: int, string: str):
        quoted_literal_regex = re.compile(
            r'^("(.(?<!(\r\n|\n.|\r.)))*")', RE_FLAGS)
        return check_result(quoted_literal_regex.search(string[start:]))


class StringLiteral(Token):
    def __init__(self, start: int, raw: str):
        super().__init__(start, raw)
        self.id = 's-string-literal'

    @staticmethod
    def match(start: int, string: str):
        string_literal_regex = re.compile(r"^([^\:\n\r])+", RE_FLAGS)
        return check_result(string_literal_regex.search(string[start:]))


class Semicolon(Token):
    def __init__(self, start: int, raw: str):
        super().__init__(start, raw)
        self.id = 'c-mapping-value'

    @staticmethod
    def match(start: int, string: str):
        return check_result(re.search(r"^:", string[start:], RE_FLAGS))


class SequenceEntry(Token):
    def __init__(self, start: int, raw: str):
        super().__init__(start, raw)
        self.id = 'c-sequence-entry'

    @staticmethod
    def match(start: int, string: str):
        return check_result(re.search(r"^-", string[start:], RE_FLAGS))

class HigherOrderToken(Token):
    def __init__(self, start: int, raw):
        self.start = start
        self.raw = raw

    def __len__(self):
        return len(self.raw)

    @property
    def value(self):
        for token in self.raw:
            if type(token.raw) == list:
                return "".join(sub_token.raw for sub_token in token.raw)
        return "".join([token.raw for token in self.raw])


class MappingKey(HigherOrderToken):
    def __init__(self, start: int, raw):
        super().__init__(start, raw)
        self.id = 'c-mapping-key'

    @property
    def value(self):
        return super().value[:-1]

    @staticmethod
    def match(start: int, token_stream):
        if start < len(token_stream) - 1 and type(token_stream[start]) == StringLiteral and type(token_stream[start + 1]) == Semicolon:
            return [token_stream[start], token_stream[start + 1]]
        return []


class Indent(HigherOrderToken):
    def __init__(self, start: int, raw):
        super().__init__(start, raw)
        self.id = 'indent'

    def __len__(self):
        return len(self.raw)

    @property
    def value(self):
        return len(self.raw[1])

    @staticmethod
    def match(start: int, token_stream):
        matched = []

        if start < len(token_stream) - 1:
            if start == 0 or type(token_stream[start]) == LineBreak:
                if type(token_stream[start]) == LineBreak:
                    matched.append(token_stream[start])
                for token in token_stream[(start if start == 0 else start + 1):]:
                    if type(token) == Space:
                        matched.append(token)
                    else:
                        break

        return matched


class SequenceItemIndent(HigherOrderToken):
    def __init__(self, start: int, raw):
        super().__init__(start, raw)
        self.id = 'sequence-indent'

    @property
    def value(self):
        return self.raw[0].value + 2

    @staticmethod
    def match(start, token_stream):
        if start < len(token_stream) - 2:
            if (type(token_stream[start]) == Indent and 
                type(token_stream[start + 1]) == SequenceEntry and 
                SequenceItemIndent.is_single_space(token_stream[start + 2])):
                return token_stream[start:start + 3]
        return []

    @staticmethod
    def is_single_space(token):
        return type(token) == Space and token.value == 1



tokens = [Space,
          LineBreak,
          StringQuotedLiteral,
          SequenceEntry,
          StringLiteral,
          Semicolon,]
