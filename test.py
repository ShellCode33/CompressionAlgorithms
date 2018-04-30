from huffman import *
from tree import *

if __name__ == "__main__":
    huffman = Huffman()
    huffman.compress(b"Coucou")
    print(huffman.characters_frequency)
    tree = Tree()
    print(tree.is_leaf())
