class Node:
    key: str
    indent: int
    children = []

    def __init__(self, key, indent, children = []):
        self.key = key
        self.indent = indent
        self.children = children


def cleanup_array_item_line(line: str):
    return line.lstrip("-").lstrip()


def get_line_indent(line: str):
    return len(line) - len(cleanup_array_item_line(line.lstrip()))


def get_key_value_raw(line: str):
    line = line.strip()
    if ":" in line:
        result = line.split(":", 1)
        key = result[0]

        value = result[1]

        return key, value
    
    return line


def is_array_item(line: str):
    if line:
        return line.startswith('-')

def subtree(line_number, parent):
    current_line = lines[line_number]
    indent = get_line_indent(current_line)

    if indent > parent.indent:
        result = get_key_value_raw(current_line)
        key = result[0]
        if is_array_item(key):
            array = Node('ARRAY', indent, [])
            parent.children.append(array)
            if ":" in current_line:
              child = Node(cleanup_array_item_line(key), indent, [])
              array.children.append(child)
              return subtree(line_number + 1, child)
            return subtree(line_number + 1, array)

        value = result[1]
        if len(value) == 0:
            child = Node(key, indent, [])
            parent.children.append(child)
            return subtree(line_number + 1, child)

        parent.children.append(Node(key, indent, value))
        return subtree(line_number + 1, parent)
    

with open("schedule.yaml") as f:
    lines = f.readlines()
    key, _ = get_key_value_raw(lines[0])
    tree = Node(key, get_line_indent(lines[0]))

    print(subtree(1, tree))
