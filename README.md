# huffmanSVG
Package for generating huffman trees in .svg format

## Installing
Install the package by running
```bash
python3 -m pip install .
```

## Usage
See the example below for usage. The set of symbols are from [this wikipedia article.](https://en.wikipedia.org/wiki/Information_theory) 
```python
    letters = {
        'a': 5, 'e': 4, 'm': 3,
        'y': 1, 'n': 2, 'i': 4,
        's': 3, 'h': 1, 'f': 1,
        'z': 1, 'o': 2, 't': 3,
        'r': 4
    }
    a = Symbols(letters)
    print(f'Self-information of the symbol "o" is: {a.information("o"):.2f}')
    print(f'Entropy of the set is: {a.entropy():.2f}')
    print(f'The huffman codes are: {a.huffmanCodes()}')
    # Encode visualization of the approach
    a.encodeSVG('huffmanTree.svg', skip=2)
```
The output is:
```txt
Self-information of the symbol "o" is: 4.09
Entropy of the set is: 3.50
The huffman codes are: {
    's': '0000',  't': '0001',  'a': '001',
    'r': '010',   'f': '01100', 'z': '01101',
    'y': '01110', 'h': '01111', 'e': '100', 
    'i': '101',   'n': '1100',  'o': '1101',
    'm': '111'}
```
![](huffmanTree.svg)