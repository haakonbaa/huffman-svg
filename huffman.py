import copy
import drawSvg as draw


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


def huffman(values: dict[str, int]) -> list[Node]:
    values = [Node(ch, val) for ch, val in values.items()]
    while len(values) > 2:
        values.sort(reverse=True, key=lambda e: e.value)
        values = values[:-2] + [Node(values[-2], values[-1])]
    values.sort(reverse=True, key=lambda e: e.value)
    return values


def traverseTree(tree: list[Node], code: str = '') -> None:
    for i, n in enumerate(tree):
        if n.isBottomNode:
            print(n.subNodes, f'{code}{i}')
        else:
            traverseTree(n.subNodes, f'{code}{i}')


padx = 20
pady = 20
radius = 15
diam = 2*radius
radius_2 = radius/2
fsize = 16


def _depthOfTree(tree: list[Node]) -> int:
    maxdepth = 0
    for n in tree:
        if n.isBottomNode:
            maxdepth = max(1, maxdepth)
        else:
            maxdepth = max(1+_depthOfTree(n.subNodes), maxdepth)
    return maxdepth

# returns number of nodes drawn


def _drawTree(tree: list[Node], x: int, y: int, drawing: draw.Drawing, depth: int = 0):
    nodesDrawn = 0
    for i, n in enumerate(tree):
        # calculate position of this node
        _startx, _starty = x, y
        _stopx, _stopy = x+(padx+diam)*nodesDrawn, y-pady-diam
        if depth == 0:
            _startx = x + (padx+diam)*nodesDrawn
        # Draw subnodes before this node
        if not n.isBottomNode:
            nodesDrawn += _drawTree(n.subNodes, x+(padx+diam)
                                    * nodesDrawn, y-pady-diam, drawing, depth + 1)
        drawing.append(draw.Line(_startx, _starty, _stopx, _stopy,
                       stroke='black', stroke_width=2, fill='none'))
        drawing.append(draw.Circle(_stopx, _stopy, radius,
                       fill='white', stroke='black', stroke_width=2))
        if n.isBottomNode:
            drawing.append(draw.Text(n.subNodes, fsize, x+(padx+diam)
                           * nodesDrawn, y-pady-diam-fsize/2, center=True, valign=True))
            nodesDrawn += 1
    return nodesDrawn


def huffmanSVG(values: dict[str, int]) -> None:
    numNodes = len(values)
    width = 3*padx+(diam+padx)*numNodes
    height = 500
    values = [Node(ch, val) for ch, val in values.items()]
    drawing = draw.Drawing(width, height, displayInline=False)

    while len(values) > 2:
        values.sort(reverse=True, key=lambda e: e.value)
        values = values[:-2] + [Node(values[-2], values[-1])]
        print(values)
        _drawTree(values, padx+radius, height-pady, drawing)
        break
    values.sort(reverse=True, key=lambda e: e.value)
    # _drawTree(values,padx,pady+radius_2,drawing,0)
    drawing.setPixelScale(2)
    drawing.saveSvg('test.svg')


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
huffmanSVG(letters)
