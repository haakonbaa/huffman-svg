"""huffman module for finding huffman codes and generating SVGs documenting
the taken approach."""

import drawSvg as draw
import math

class Symbols():
    def __init__(self, symbols : dict):
        self.symbols = symbols
        self._sumFreq = sum(symbols.values())
    
    def I(self, symbol : str):
        if symbol not in self.symbols:
            return 0
        return math.log2(self._sumFreq/self.symbols[symbol])

    def H(self):
        return sum(freq/self._sumFreq*self.I(s) for s,freq in self.symbols.items())

    def __repr__(self):
        return f'Symbols({self.symbols})'


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


# Takes a dict with characters and corresponding frequencies, creating a tree
# represented by a list of Nodes
def huffman(values: dict[str, int]) -> list[Node]:
    values = [Node(ch, val) for ch, val in values.items()]
    while len(values) > 2:
        values.sort(reverse=True, key=lambda e: e.value)
        values = values[:-2] + [Node(values[-2], values[-1])]
    values.sort(reverse=True, key=lambda e: e.value)
    return values


# Traverses a tree represented by lists of nodes and returns the code for each
# character in the tree
def traverseTree(tree: list[Node], code: str = '', result={}) -> dict:
    for i, n in enumerate(tree):
        if n.isBottomNode:
            result[n.subNodes] = f'{code}{i}'
        else:
            traverseTree(n.subNodes, f'{code}{i}', result)
    return result


padx = 15
pady = 15
radius = 10
diam = 2*radius
radius_2 = radius/2
fsize = 12

# returns depth of tree represented by list of Nodes
def _depthOfTree(tree: list[Node]) -> int:
    maxdepth = 0
    for n in tree:
        if n.isBottomNode:
            maxdepth = max(1, maxdepth)
        else:
            maxdepth = max(1+_depthOfTree(n.subNodes), maxdepth)
    return maxdepth

# Draws a tree on given coordinates
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
        drawing.append(draw.Text(str(n.value), fsize,
                       (_startx+_stopx)/2+padx/4, (_starty+_stopy)/2-pady/4))
        if n.isBottomNode:
            drawing.append(draw.Text(n.subNodes, fsize, x+(padx+diam)
                           * nodesDrawn, y-pady-diam-fsize/2, center=True, valign=True))
            nodesDrawn += 1
    return nodesDrawn

# Takes a dict with characters and corresponding frequencies creating an svg
# representing how to make a huffman-code from it.
def huffmanSVG(values: dict[str, int]) -> None:
    numNodes = len(values)
    width = 2*padx+diam+(diam+padx)*(numNodes-1)
    height = 500
    values = [Node(ch, val) for ch, val in values.items()]
    drawing = draw.Drawing(width, height, displayInline=False)
    offsetY = 0
    iters = -1

    values.sort(reverse=True, key=lambda e: e.value)
    while len(values) > 2:
        iters += 1
        if iters % 2 != 0:
            continue
        values = values[:-2] + [Node(values[-2], values[-1])]
        values.sort(reverse=True, key=lambda e: e.value)
        drawing.append(draw.Line(padx, height-pady-offsetY, width-padx, height-pady-offsetY,
                       stroke='black', stroke_width=2, fill='none'))
        _drawTree(values, padx+radius, height-pady-offsetY, drawing)
        offsetY += (_depthOfTree(values)+1)*(diam+pady)
    # values.sort(reverse=True, key=lambda e: e.value)
    # drawing.append(draw.Line(padx, height-pady-offsetY, width-padx, height-pady-offsetY,
    #                          stroke='black', stroke_width=2, fill='none'))
    # _drawTree(values, padx+radius, height-pady-offsetY, drawing)
    drawing.height = 2*pady+offsetY
    drawing.viewBox = (0, height-offsetY) + (width, drawing.height)
    drawing.viewBox = (drawing.viewBox[0], -drawing.viewBox[1]-drawing.viewBox[3],
                       drawing.viewBox[2], drawing.viewBox[3])
    drawing.setPixelScale(2)
    drawing.saveSvg('huffman.svg')

def mdTableHuffman(tree: list[Node]) -> str:
    result = '|char|code|\n|-|-|\n'
    result += '\n'.join(f'|{c}|{v}|' for c,v in traverseTree(tree).items())
    print(result)



def main():
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
    a = Symbols(letters)
    print(a.H()) 

    print(traverseTree(huffman(letters)))
    huffmanSVG(letters)
    mdTableHuffman(huffman(letters))


if __name__ == '__main__':
    main()
