import copy


class Node:
    # n1 and n2 are respectively Node and Node
    # or character and value pair
    def __init__(self, n1, n2):
        if isinstance(n1, Node) and isinstance(n2, Node):
            self.value = n1.value + n2.value
            self.subNodes = [n1, n2]
            self.isBottomNode = False
            return

        self.value = n2
        self.subNodes = str(n1)
        self.isBottomNode = True

    def __str__(self):
        return f'[{self.value},{str(self.subNodes)}]'

    def __repr__(self):
        return str(self)

    def __lt__(self, rhs):
        return self.value < rhs.value

    def __gt__(self, rhs):
        return self.value > rhs.value

    def __eq__(self, rhs):
        return self.value == rhs.value


def huffman(values: dict[str, int]):
    values = [Node(ch, val) for ch, val in values.items()]
    while len(values) > 2:
        values.sort(reverse=True, key=lambda e: e.value)
        values = values[:-2] + [Node(values[-2], values[-1])]
        print(values)
    values.sort(reverse=True, key=lambda e: e.value)
    return values


def traverseTree(tree, code=''):
    for i, n in enumerate(tree):
        if n.isBottomNode:
            print(n.subNodes, f'{code}{i}')
        else:
            traverseTree(n.subNodes, f'{code}{i}')


letters = {
    'a': 5,
    'e': 4,
    'm': 3,
    'y': 1,
    'n': 2,
    'i': 4,
    's': 3,
    'h': 1,
    'f': 1,
    'z': 1,
    'o': 2,
    't': 3,
    'r': 4
}
traverseTree(huffman(letters))
