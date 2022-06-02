"""huffman module for finding huffman codes and generating SVGs documenting
the taken approach."""

import drawSvg
import math


class Node:
    """class representing a node in a huffman tree"""

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


class Symbols():
    """Class representing a set of symbols and their corresponding whole-number frequencies"""

    def __init__(self, symbols: dict):
        self.symbols = {str(key): int(value)
                        for key, value in symbols.items()}
        self._sumFreq = sum(symbols.values())

    def information(self, symbol: str) -> float:
        """returns the self-information of a symbol"""
        if symbol not in self.symbols:
            return 0.0
        return math.log2(self._sumFreq/self.symbols[symbol])

    def entropy(self) -> float:
        """returns the entropy of the set of symbols"""
        return sum(freq/self._sumFreq*self.information(s) for s, freq in self.symbols.items())

    def huffmanCodes(self) -> dict:
        """returns a dict of huffman codes generated from the set"""
        tree = _huffman(self.symbols)
        return _huffmanCodesTree(tree)

    def encodeSVG(self, filename: str, skip=3):
        """generate an svg representing how to find the huffman codes. skip is how many steps to skip each frame"""
        _huffmanSVG(self.symbols, filename, skip)

    def __repr__(self):
        return f'Symbols({self.symbols})'


def _huffman(values: dict) -> list[Node]:
    """generates a huffman tree represented by a list of Nodes from a dict"""
    values = [Node(ch, val) for ch, val in values.items()]
    while len(values) > 2:
        values.sort(reverse=True, key=lambda e: e.value)
        values = values[:-2] + [Node(values[-2], values[-1])]
    values.sort(reverse=True, key=lambda e: e.value)
    return values


def _huffmanCodesTree(tree: list[Node], code: str = '', result={}) -> dict:
    """returns the huffman code for each character in in tree represented by list of Nodes"""
    for i, n in enumerate(tree):
        if n.isBottomNode:
            result[n.subNodes] = f'{code}{i}'
        else:
            _huffmanCodesTree(n.subNodes, f'{code}{i}', result)
    return result


padx = 15
pady = 15
radius = 10
diam = 2*radius
radius_2 = radius/2
fsize = 12


def _depthOfTree(tree: list[Node]) -> int:
    """returns the depth of a tree represented by a list of Nodes"""
    maxdepth = 0
    for n in tree:
        if n.isBottomNode:
            maxdepth = max(1, maxdepth)
        else:
            maxdepth = max(1+_depthOfTree(n.subNodes), maxdepth)
    return maxdepth

# Draws a tree on given coordinates


def _drawTree(tree: list[Node], x: int, y: int, drawing: drawSvg.Drawing, depth: int = 0):
    """draws a huffman tree from a given list of Nodes """
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
        drawing.append(drawSvg.Line(_startx, _starty, _stopx, _stopy,
                       stroke='black', stroke_width=2, fill='none'))
        drawing.append(drawSvg.Circle(_stopx, _stopy, radius,
                       fill='white', stroke='black', stroke_width=2))
        drawing.append(drawSvg.Text(str(n.value), fsize,
                       (_startx+_stopx)/2+padx/4, (_starty+_stopy)/2-pady/4))
        if n.isBottomNode:
            drawing.append(drawSvg.Text(n.subNodes, fsize, x+(padx+diam)
                           * nodesDrawn, y-pady-diam-fsize/2, center=True, valign=True))
            nodesDrawn += 1
    return nodesDrawn


def _huffmanSVG(values: dict[str, int], filename: str, skip) -> None:
    """generates an .svg representing the how to find the huffman tree of a set"""
    numNodes = len(values)
    width = 2*padx+diam+(diam+padx)*(numNodes-1)
    height = 500
    values = [Node(ch, val) for ch, val in values.items()]
    drawing = drawSvg.Drawing(width, height, displayInline=False)
    offsetY = 0
    iters = -1

    values.sort(reverse=True, key=lambda e: e.value)
    while len(values) > 2:
        iters += 1
        if iters % skip != 0:
            continue
        values = values[:-2] + [Node(values[-2], values[-1])]
        values.sort(reverse=True, key=lambda e: e.value)
        drawing.append(drawSvg.Line(padx, height-pady-offsetY, width-padx, height-pady-offsetY,
                       stroke='black', stroke_width=2, fill='none'))
        _drawTree(values, padx+radius, height-pady-offsetY, drawing)
        offsetY += (_depthOfTree(values)+1)*(diam+pady)
    drawing.height = 2*pady+offsetY
    drawing.viewBox = (0, height-offsetY) + (width, drawing.height)
    drawing.viewBox = (drawing.viewBox[0], -drawing.viewBox[1]-drawing.viewBox[3],
                       drawing.viewBox[2], drawing.viewBox[3])
    drawing.setPixelScale(2)
    drawing.saveSvg(filename)


def _mdTableHuffman(tree: list[Node]) -> str:
    result = '|char|code|\n|-|-|\n'
    result += '\n'.join(f'|{c}|{v}|' for c,
                        v in _huffmanCodesTree(tree).items())
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
    print(a.information('o'))
    print(a.entropy())
    print(a.huffmanCodes())
    a.encodeSVG('huffmanTree.svg')


if __name__ == '__main__':
    main()
