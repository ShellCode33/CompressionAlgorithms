#!/usr/bin/python3
# coding: utf-8

from huffman import Huffman

if __name__ == "__main__":
    huffman = Huffman()
    huffman.compress_file("/tmp/huffman", "/tmp/huffman_encoded")
