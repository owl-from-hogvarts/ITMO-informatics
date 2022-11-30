from scanner import tokens, token_scanner, scanner, Indent, StringLiteral, StringQuotedLiteral, SequenceItemIndent, MappingKey, Space

ARRAY_ENTRY = 'ARRAY_ENTRY'

class Node:
    def __init__(self, key, children=[]):
        self.key = key
        self.children = children

    def __str__(self):
        if self.key == 'VALUE':
            return str(self.children[0])

        node_content = ''
        for child in self.children:
            node_content += "\n".join(['  ' + s for s in filter(None, str(child).split("\n"))]) + "\n"

        key = self.key.replace(" ", "-")
        return f'<{key}>\n{node_content}\n</{key}>\n'

with open("schedule.yaml") as f:
    content = f.read()

    def token_stream_filter(token_stream):
        return list(filter(lambda token : type(token) != Space, token_stream))

    current_token_cursor = 0
    token_stream = token_scanner([SequenceItemIndent] ,token_scanner([MappingKey, Indent], scanner(tokens, content)))
    token_stream = token_stream_filter(token_stream)

    def next_token(offset=1):
        global current_token_cursor
        token = token_stream[current_token_cursor + offset - 1]
        current_token_cursor += offset
        return token

    def preview_next_token():
        return token_stream[current_token_cursor]

    def check_next_token(Token, offset=0):
        token = token_stream[current_token_cursor + offset]
        return type(token) == Token

    def tree(parent, parent_indent):
        if check_next_token(StringLiteral) or check_next_token(StringQuotedLiteral):
            map_value = next_token()
            return parent.children.append(Node('VALUE', [map_value.value]))
        
        sequence_item_last_indent = 0
        while check_next_token(SequenceItemIndent):
            next_token_indent = next_token()
            if next_token_indent.value > parent_indent:
                array_entry_node = Node(ARRAY_ENTRY, [])
                parent.children.append(array_entry_node)
                tree(array_entry_node, next_token_indent.value)
            else:
                return
        
        while check_next_token(Indent) or check_next_token(MappingKey):
            if check_next_token(Indent):
                token = preview_next_token()
                if token.value > parent_indent or (parent.key == ARRAY_ENTRY and token.value == parent_indent):
                    key_token = next_token(2)
                    key_node = Node(key_token.value, [])
                    parent.children.append(key_node)
                    tree(key_node, token.value)
                else:
                    return
            else:
                key_token = next_token()
                key_node = Node(key_token.value, [])
                parent.children.append(key_node)
                tree(key_node, parent_indent)
    root = Node('ROOT', [])
    tree(root, 0)

    print(root, file=open("xml_from_yaml_hard.xml", "w", encoding="utf-8"))
    
