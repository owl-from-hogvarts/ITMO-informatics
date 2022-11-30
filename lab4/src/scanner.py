
from utils.spaces import is_s_space
from utils.breaking_symbols import is_b_carriage_return, is_b_line_feed
from utils.symbols import is_nb_char, is_c_double_quote, is_c_mapping_value, is_c_sequence_entry


# Abstract


class Token:
    def __init__(self, start: int, raw: str):
        self.start = start
        self.raw = raw

    def __len__(self):
        return len(self.raw)

    @property
    def value(self):
        return self.raw


class Space(Token):
    def __init__(self, start, raw: str):
        super().__init__(start, raw)
        self.id = 's-space'

    @property
    def value(self):
        return len(self.raw)

    @staticmethod
    def match(start: int, string: str):
        chars = []
        for char in string[start:]:
            if is_s_space(char):
                chars.append(char)
            else:
                break
        return "".join(chars)


class LineBreak(Token):
    def __init__(self, start: int, raw: str):
        super().__init__(start, raw)
        self.id = 'b-break'

    @staticmethod
    def match(start: int, string: str):
        next_char_position = start + 1
        if len(string[start:]) > 0:
            if is_b_carriage_return(string[start]) and is_b_line_feed(string[next_char_position]):
                return string[start: next_char_position + 1]  # to be inclusive

        if is_b_carriage_return(string[start]) or is_b_line_feed(string[start]):
            return string[start]

        return ""


class StringQuotedLiteral(Token):
    def __init__(self, start: int, raw: str):
        super().__init__(start, raw)
        self.id = 's-string-literal-quoted'

    @property
    def value(self):
        return self.raw[1:-1]

    @staticmethod
    def match(start: int, string: str):
        matched = []

        if is_c_double_quote(string[start]):
            matched.append('"')
            for char in string[start + 1:]:
                if is_nb_char(char) and not is_c_double_quote(char):
                    matched.append(char)
                elif is_c_double_quote(char):
                    break
            matched.append('"')
        return "".join(matched)


class StringLiteral(Token):
    def __init__(self, start: int, raw: str):
        super().__init__(start, raw)
        self.id = 's-string-literal'

    @staticmethod
    def match(start: int, string: str):
        matched = []
        for char in string[start:]:
            if is_nb_char(char) and not is_c_double_quote(char) and not is_c_mapping_value(char):
                matched.append(char)
                continue

            break

        return "".join(matched)


class Semicolon(Token):
    def __init__(self, start: int, raw: str):
        super().__init__(start, raw)
        self.id = 'c-mapping-value'

    @staticmethod
    def match(start: int, string: str):
        if is_c_mapping_value(string[start]):
            return string[start]

        return ""


class SequenceEntry(Token):
    def __init__(self, start: int, raw: str):
        super().__init__(start, raw)
        self.id = 'c-sequence-entry'

    @staticmethod
    def match(start: int, string: str):
        char = string[start]
        if is_c_sequence_entry(char):
            return char

        return ""


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


def scanner(tokens, input):
    cursor = 0
    token_stream = []

    while cursor < len(input):
        something_matched = False
        for Token in tokens:
            # if at least one char match, try to create token
            token_content = Token.match(cursor, input)
            if len(token_content):
                token = Token(cursor, token_content)
                something_matched = True
                cursor += len(token)
                token_stream.append(token)
                break
        if not something_matched:
            cursor += 1

    return token_stream


def token_scanner(tokens, token_stream_input):
    cursor = 0
    token_stream = list(token_stream_input)

    while cursor < len(token_stream_input):
        something_matched = False
        for Token in tokens:
            # if at least one char match, try to create token
            token_content = Token.match(cursor, token_stream)
            if len(token_content):
                token = Token(cursor, token_content)
                something_matched = True
                token_stream = token_stream[:cursor] + \
                    [token] + token_stream[cursor + len(token):]

                cursor += 1
                break
        if not something_matched:
            cursor += 1

    return token_stream


tokens = [Space, LineBreak, StringQuotedLiteral,
          SequenceEntry, StringLiteral, Semicolon]